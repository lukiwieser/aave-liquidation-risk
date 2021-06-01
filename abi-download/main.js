const LendingPoolV2Artifact = require('@aave/protocol-v2/artifacts/contracts/protocol/lendingpool/LendingPool.sol/LendingPool.json');
const fs = require('fs')

// Log the ABI into console
//console.log(LendingPoolV2Artifact.abi)

fs.writeFileSync("out.json", LendingPoolV2Artifact.abi)