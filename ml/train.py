"""Train a reproducible frozen-MobileNetV3 CNN + learned linear classifier."""
import os, json, random, hashlib, time, shutil
from pathlib import Path
import numpy as np
import torch
from torch import nn
from torchvision import models, transforms
from PIL import Image
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

ROOT=Path(__file__).resolve().parents[1]; DATA=Path(os.environ.get('DATASET_DIR','/workspace/work/dataset-resized'))
OUT=ROOT/'dist'; (OUT/'model').mkdir(exist_ok=True); (OUT/'samples').mkdir(exist_ok=True)
random.seed(42); np.random.seed(42); torch.manual_seed(42); torch.set_num_threads(3)
classes=['cardboard','glass','metal','paper','plastic','trash']
files=[]; labels=[]; seen=set(); duplicates=[]
for i,c in enumerate(classes):
 for p in sorted((DATA/c).glob('*.jpg')):
  digest=hashlib.sha256(p.read_bytes()).hexdigest()
  if digest in seen: duplicates.append(str(p)); continue
  seen.add(digest); files.append(p); labels.append(i)
idx=np.arange(len(files)); train_idx,temp=train_test_split(idx,test_size=.30,stratify=labels,random_state=42)
val_idx,test_idx=train_test_split(temp,test_size=.5,stratify=np.array(labels)[temp],random_state=42)
json.dump({k:[str(files[i].relative_to(DATA)) for i in ids] for k,ids in [('train',train_idx),('validation',val_idx),('test',test_idx)]},open(ROOT/'ml/splits.json','w'),indent=2)
base=models.mobilenet_v3_small(weights=models.MobileNet_V3_Small_Weights.IMAGENET1K_V1).eval()
encoder=nn.Sequential(base.features,base.avgpool,nn.Flatten()).eval()
for p in encoder.parameters(): p.requires_grad=False
norm=transforms.Normalize([.485,.456,.406],[.229,.224,.225])
plain=transforms.Compose([transforms.Resize((160,160)),transforms.ToTensor(),norm])
aug=transforms.Compose([transforms.Resize((180,180)),transforms.RandomResizedCrop(160,scale=(.75,1.)),transforms.RandomHorizontalFlip(),transforms.ColorJitter(.15,.15,.10,.02),transforms.ToTensor(),norm])
def extract(ids,tf):
 chunks=[]
 for start in range(0,len(ids),32):
  batch=torch.stack([tf(Image.open(files[i]).convert('RGB')) for i in ids[start:start+32]])
  with torch.inference_mode(): chunks.append(encoder(batch))
 return torch.cat(chunks)
start=time.time(); print('Extracting frozen CNN features',flush=True)
x=torch.cat([extract(train_idx,plain),extract(train_idx,aug),extract(train_idx,aug)])
y=torch.tensor(np.tile(np.array(labels)[train_idx],3)); xv=extract(val_idx,plain); yv=torch.tensor(np.array(labels)[val_idx]); xt=extract(test_idx,plain)
head=nn.Linear(576,6); opt=torch.optim.AdamW(head.parameters(),lr=.003,weight_decay=.02)
weights=torch.tensor(len(train_idx)/(6*np.bincount(np.array(labels)[train_idx])),dtype=torch.float32)
lossfn=nn.CrossEntropyLoss(weight=weights); history=[]; best=1e9
for epoch in range(1,81):
 head.train(); total=0
 for ids in torch.randperm(len(x)).split(128):
  opt.zero_grad(); loss=lossfn(head(x[ids]),y[ids]); loss.backward(); opt.step(); total+=loss.item()*len(ids)
 head.eval()
 with torch.no_grad():
  logits=head(xv); vl=nn.functional.cross_entropy(logits,yv).item(); va=(logits.argmax(1)==yv).float().mean().item()
 history.append({'epoch':epoch,'train_loss':total/len(x),'val_loss':vl,'val_accuracy':va})
 if vl<best: best=vl; best_epoch=epoch; torch.save(head.state_dict(),ROOT/'ml/head.pt')
 if epoch%10==0: print('Epoch',epoch,'validation accuracy',round(va,4),flush=True)
head.load_state_dict(torch.load(ROOT/'ml/head.pt',weights_only=True)); model=nn.Sequential(encoder,head).eval()
with torch.no_grad(): pred=head(xt).argmax(1).numpy()
yt=np.array(labels)[test_idx]; report=classification_report(yt,pred,target_names=classes,output_dict=True,zero_division=0)
metrics={'classes':classes,'dataset_count':len(files),'exact_duplicates_removed':len(duplicates),'split':{'train':len(train_idx),'validation':len(val_idx),'test':len(test_idx)},'seed':42,'best_epoch':best_epoch,'accuracy':accuracy_score(yt,pred),'report':report,'confusion_matrix':confusion_matrix(yt,pred).tolist(),'history':history,'seconds':round(time.time()-start),'parameters':sum(p.numel() for p in model.parameters()),'trainable_parameters':sum(p.numel() for p in head.parameters())}
json.dump(metrics,open(OUT/'metrics.json','w'),indent=2)
json.dump({'classes':classes,'size':160,'mean':[.485,.456,.406],'std':[.229,.224,.225]},open(OUT/'model/config.json','w'),indent=2)
torch.save(model.state_dict(),ROOT/'ml/model.pt')
torch.onnx.export(model,torch.zeros(1,3,160,160),str(OUT/'model/sortloop.onnx'),input_names=['image'],output_names=['logits'],opset_version=17,dynamo=False)
samples=[]
for c in range(6):
 i=next(i for i in test_idx if labels[i]==c); dest=OUT/'samples'/f'{classes[c]}.jpg'; shutil.copy(files[i],dest); samples.append({'class':classes[c],'file':f'samples/{classes[c]}.jpg','source':str(files[i].relative_to(DATA))})
json.dump(samples,open(OUT/'samples/index.json','w'),indent=2)
# Verify exported inference against the training framework.
import onnxruntime as ort
session=ort.InferenceSession(str(OUT/'model/sortloop.onnx')); image=plain(Image.open(files[test_idx[0]]).convert('RGB')).unsqueeze(0)
with torch.no_grad(): expected=model(image).numpy()
actual=session.run(None,{'image':image.numpy()})[0]; delta=float(np.max(np.abs(expected-actual))); assert delta<1e-4
json.dump({'max_logit_error':delta,'passed':True},open(ROOT/'ml/export-check.json','w'),indent=2)
print(json.dumps({k:v for k,v in metrics.items() if k not in ['history','report','confusion_matrix']}),flush=True)
