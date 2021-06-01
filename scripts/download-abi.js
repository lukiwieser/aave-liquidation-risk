const LendingPoolV2Artifact = require('@aave/protocol-v2/artifacts/contracts/protocol/lendingpool/LendingPool.sol/LendingPool.json');
const fs = require('fs')

fs.writeFileSync("../data/raw/abi.json", JSON.stringify(LendingPoolV2Artifact.abi))