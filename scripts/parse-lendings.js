const InputDataDecoder = require('ethereum-input-data-decoder');
const csv = require('csv-parser');
const fs = require('fs');
const createCsvWriter = require('csv-writer').createObjectCsvWriter;


const decoder = new InputDataDecoder("../data/raw/abi.json");

const data = []
count = 0;

fs.createReadStream('../data/raw/tx-history-short.csv')
  .pipe(csv())
  .on('data', (row) => {
    newRow = {...row}
    const result = decoder.decodeData(row.input);
    row.input_decoded = JSON.stringify(result);
    data.push(row)
    
    count++
    //if(count % 1000 === 0) console.log(count);
  })
  .on('end', () => {
    console.log('CSV file successfully processed');

    const csvWriter = createCsvWriter({
      path: '../data/parsed/tx-history.csv',
      fieldDelimiter: ';',
      header: [
        {id: 'timestamp', title: 'timestamp'},
        {id: 'hash', title: 'hash'},
        {id: 'input', title: 'input'},
        {id: 'input_decoded', title: 'input_decoded'},
      ]
    });

    csvWriter.writeRecords(data).then(
      ()=> console.log('The CSV file was written successfully')
    );
  });