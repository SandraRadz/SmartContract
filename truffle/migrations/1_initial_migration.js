const Escrow = artifacts.require("Escrow");

module.exports = function (deployer) {
  deployer.deploy(Escrow, "0x5B38Da6a701c568545dCfcB03FcB875f56beddC4", "0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2", "1");
};
