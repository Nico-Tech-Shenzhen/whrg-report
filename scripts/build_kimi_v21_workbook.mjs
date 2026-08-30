// Author the prepared candidate with @oai/artifact-tool; no input workbook is saved.
// Copy this file beside spec.json and a junction to the bundled node_modules.
import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { SpreadsheetFile, Workbook } from '@oai/artifact-tool';

const work = path.dirname(fileURLToPath(import.meta.url));
const spec = JSON.parse(await fs.readFile(path.join(work, 'spec.json'), 'utf8'));
const wb = Workbook.create();
const col = n => { let s=''; for (;n>0;n=Math.floor((n-1)/26)) s=String.fromCharCode(65+(n-1)%26)+s; return s; };
const previews = path.join(work, 'previews');
await fs.mkdir(previews, {recursive:true});
for (let i=0;i<spec.sheets.length;i++) {
  const data=spec.sheets[i];
  const sheet=wb.worksheets.add(data.name);
  sheet.showGridLines=false;
  const matrix=[data.headers,...data.rows];
  // Values, never formulas: source text remains inert.
  for (const row of matrix) for (const v of row) {
    if (typeof v==='string' && v.startsWith('=')) throw new Error('Literal formula prefix needs explicit handling');
  }
  const last=matrix.length;
  const range=sheet.getRange(`A1:${col(data.headers.length)}${last}`);
  range.values=matrix;
  range.format.font.name='Yu Gothic';
  range.format.font.size=10;
  range.format.columnWidth=22;
  range.format.rowHeight=48;
  range.format.wrapText=true;
  range.format.verticalAlignment='top';
  range.setNumberFormat('@');
  const header=sheet.getRange(`A1:${col(data.headers.length)}1`);
  header.format={fill:'#173A4B',font:{bold:true,color:'#FFFFFF',size:10},rowHeight:42,wrapText:true,verticalAlignment:'center'};
  for (let j=0;j<data.headers.length;j++) {
    const label=data.headers[j];
    let width=/JSON/.test(label)?68:/Text|Evidence$|Summary|Notes|Question$|Basis|Details|Meaning|Value|Label|Title|Finding|Payload/i.test(label)?48:24;
    if (/^ID$|Supplied ID|Entry ID|Competition ID|Question ID/.test(label)) width=23;
    if (label==='Original Chinese Evidence' || label==='Japanese Summary' || label==='text') width=76;
    sheet.getRange(`${col(j+1)}1:${col(j+1)}${last}`).format.columnWidth=width;
  }
  if (last>1) {
    const table=sheet.tables.add(`A1:${col(data.headers.length)}${last}`,true,`CandidateTable${i+1}`);
    table.showBandedRows=true;
    const status=data.headers.indexOf('Participation Status');
    if(status>=0) sheet.getRange(`${col(status+1)}2:${col(status+1)}${last}`).dataValidation={rule:{type:'list',values:['Registered','Scheduled','Started','Finished','DNF','DNS','Disqualified','Unknown']}};
    const verification=data.headers.indexOf('Verification Status');
    if(verification>=0) {
      const vr=sheet.getRange(`${col(verification+1)}2:${col(verification+1)}${last}`);
      vr.dataValidation={rule:{type:'list',values:['Verified','Research Lead']}};
      vr.conditionalFormats.add('containsText',{text:'Research Lead',format:{fill:'#FFF0CE',font:{color:'#815600'}}});
    }
    if (data.name==='Read Me') sheet.getRange(`B2:B${last}`).format.columnWidth=112;
    if (data.name==='Evidence Text Contents') {
      sheet.getRange(`D2:D${last}`).format.columnWidth=90;
      sheet.getRange(`A2:E${last}`).format.rowHeight=95;
    }
    if (data.name==='Field Evidence') sheet.getRange(`A2:G${last}`).format.rowHeight=160;
    if (data.name==='Verification Review') sheet.getRange(`A2:G${last}`).format.rowHeight=150;
    if (data.name==='Competition Entry Map') sheet.getRange(`A2:Z${last}`).format.rowHeight=135;
    if (data.name==='Evidence Map') {
      for(let r=0;r<data.rows.length;r++) {
        const text=String(data.rows[r][7]||'');
        sheet.getRange(`A${r+2}:T${r+2}`).format.rowHeight=Math.max(56,Math.min(360,20*(Math.ceil(text.length/64)+2)));
      }
    }
  }
  sheet.freezePanes.freezeRows(1);
  sheet.freezePanes.freezeColumns(Math.min(2,data.headers.length));
  const endColumn=col(Math.min(4,data.headers.length));
  const preview=await wb.render({sheetName:data.name,range:`A1:${endColumn}${Math.min(last,5)}`,format:'png',scale:1});
  await fs.writeFile(path.join(previews,`${String(i+1).padStart(2,'0')}.png`),new Uint8Array(await preview.arrayBuffer()));
  console.log(`Prepared and rendered: ${data.name} (${data.rows.length} rows)`);
}
for (const [name,range,file] of [
  ['Evidence Map','G1:L5','evidence-text.png'],
  ['Competition Entry Map','N1:U8','entry-states.png'],
  ['Verification Review','A1:F7','verification.png'],
]) {
  const image=await wb.render({sheetName:name,range,format:'png',scale:1});
  await fs.writeFile(path.join(previews,file),new Uint8Array(await image.arrayBuffer()));
}
console.log((await wb.inspect({kind:'sheet',include:'id,name',maxChars:6000})).ndjson);
const output=await SpreadsheetFile.exportXlsx(wb);
await output.save(path.resolve(work,'..','WHRG_2026_Master_v2_1.xlsx'));
console.log('Exported candidate; canonical corpus untouched.');
