const InputDataDecoder = require('ethereum-input-data-decoder');
const csv = require('csv-parser');
const fs = require('fs');
const createCsvWriter = require('csv-writer').createObjectCsvWriter;
const getDirName = require('path').dirname;

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
    if(count % 10000 === 0) console.log(count);
  })
  .on('end', () => {
    console.log('CSV file successfully processed');

    const csvWriter = createCsvWriter({
      path: '../data/parsed/tx-history-short.csv',
      fieldDelimiter: ';',
      header: [
        {id: 'timestamp', title: 'timestamp'},
        {id: 'blockNumber', title: 'blockNumber'},
        {id: 'hash', title: 'hash'},
        {id: 'from', title: 'from'},
        {id: 'to', title: 'to'},
        {id: 'input', title: 'input'},
        {id: 'input_decoded', title: 'input_decoded'},
        {id: 'isError', title: 'isError'},
        {id: 'txreceipt_status', title: 'txreceipt_status'},
      ]
    });

    fs.mkdir(getDirName('../data/parsed/tx-history.csv'), { recursive: true}, function (err) {
        if (err) return cb(err);
    });

    csvWriter.writeRecords(data).then(
      ()=> console.log('CSV file successfully saved to data/parsed')
    );
  });