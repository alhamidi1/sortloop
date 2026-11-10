const fs=require('fs');for(const f of ['index.html','style.css','app.js'])fs.copyFileSync('src/'+f,'dist/'+f);console.log('Static application built.');
