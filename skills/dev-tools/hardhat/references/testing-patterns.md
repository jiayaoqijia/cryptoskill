# Hardhat Testing Patterns

## Test Structure

```typescript
import { expect } from "chai";
import { ethers } from "hardhat";
import { loadFixture } from "@nomicfoundation/hardhat-toolbox/network-helpers";

describe("Contract", function () {
  // Fixture for consistent test setup
  async function deployFixture() {
    const [owner, addr1, addr2] = await ethers.getSigners();
    const Contract = await ethers.getContractFactory("MyContract");
    const contract = await Contract.deploy("Initial");
    return { contract, owner, addr1, addr2 };
  }

  describe("Deployment", function () {
    it("Should set initial values", async function () {
      const { contract, owner } = await loadFixture(deployFixture);
      expect(await contract.owner()).to.equal(owner.address);
    });
  });
});
```

## Testing Events

```typescript
it("Should emit event", async function () {
  const { contract } = await loadFixture(deployFixture);

  await expect(contract.setValue(100))
    .to.emit(contract, "ValueChanged")
    .withArgs(0, 100);
});
```

## Testing Reverts

```typescript
it("Should revert with message", async function () {
  const { contract, addr1 } = await loadFixture(deployFixture);

  await expect(
    contract.connect(addr1).onlyOwnerFunction()
  ).to.be.revertedWith("Not owner");
});

it("Should revert with custom error", async function () {
  await expect(contract.withdraw())
    .to.be.revertedWithCustomError(contract, "InsufficientBalance")
    .withArgs(0, 100);
});
```

## Time Manipulation

```typescript
import { time } from "@nomicfoundation/hardhat-toolbox/network-helpers";

it("Should work after time passes", async function () {
  // Increase time by 1 day
  await time.increase(86400);

  // Set to specific timestamp
  await time.increaseTo(1893456000);

  // Get latest block timestamp
  const latest = await time.latest();
});
```

## Testing with Different Accounts

```typescript
it("Should work with different signers", async function () {
  const { contract, addr1 } = await loadFixture(deployFixture);

  // Connect as different account
  await contract.connect(addr1).publicFunction();
});
```

## Snapshot and Revert

```typescript
import { takeSnapshot } from "@nomicfoundation/hardhat-toolbox/network-helpers";

it("Should restore state", async function () {
  const snapshot = await takeSnapshot();

  // Make changes
  await contract.setValue(100);

  // Restore to snapshot
  await snapshot.restore();

  expect(await contract.value()).to.equal(0);
});
```
