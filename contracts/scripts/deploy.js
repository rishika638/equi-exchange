const hre = require("hardhat");

async function main() {
  const EquiExchange = await ethers.getContractFactory("EquiExchangeRecords");
  const equiExchange = await EquiExchange.deploy();

  await equiExchange.deployed(); // ✅ ethers v5 way

  console.log("EquiExchange deployed to:", equiExchange.address);
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });

