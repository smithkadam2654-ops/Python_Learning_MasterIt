"""
Blockchain Advanced Module

This module provides comprehensive advanced blockchain utilities including:
- Smart contract concepts
- Merkle tree implementation
- Blockchain consensus algorithms
- Cryptographic utilities
- Transaction processing
- Block validation
- Wallet management
- Gas calculation
- State management
- Blockchain networking concepts

Note: This module uses cryptography libraries for advanced features.
Install with: pip install cryptography ecdsa

All functions include comprehensive docstrings and type hints.
"""

import hashlib
import json
import time
from typing import Any, Dict, List, Optional, Tuple, Union
from dataclasses import dataclass
from enum import Enum
from collections import defaultdict


try:
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.asymmetric import ec
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.backends import default_backend
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False

try:
    import ecdsa
    ECDSA_AVAILABLE = True
except ImportError:
    ECDSA_AVAILABLE = False


class ConsensusType(Enum):
    """Types of consensus algorithms."""
    PROOF_OF_WORK = "proof_of_work"
    PROOF_OF_STAKE = "proof_of_stake"
    PROOF_OF_AUTHORITY = "proof_of_authority"
    DELEGATED_PROOF_OF_STAKE = "delegated_proof_of_stake"


class TransactionType(Enum):
    """Types of transactions."""
    TRANSFER = "transfer"
    CONTRACT_CALL = "contract_call"
    CONTRACT_DEPLOY = "contract_deploy"
    STAKE = "stake"
    UNSTAKE = "unstake"


@dataclass
class MerkleNode:
    """Merkle tree node."""
    hash: str
    left: Optional['MerkleNode'] = None
    right: Optional['MerkleNode'] = None


@dataclass
class SmartContract:
    """Smart contract data structure."""
    address: str
    code: str
    storage: Dict[str, Any]
    owner: str
    balance: int = 0
    
    def call(self, function: str, args: List[Any]) -> Any:
        """Call contract function (simplified)."""
        # In real implementation, this would execute bytecode
        return f"Called {function} with args {args}"
    
    def set_storage(self, key: str, value: Any) -> None:
        """Set contract storage."""
        self.storage[key] = value
    
    def get_storage(self, key: str) -> Any:
        """Get contract storage."""
        return self.storage.get(key)


@dataclass
class Transaction:
    """Transaction data structure."""
    tx_id: str
    from_address: str
    to_address: str
    amount: int
    transaction_type: TransactionType
    timestamp: float
    gas_limit: int = 21000
    gas_used: int = 0
    gas_price: int = 1
    data: str = ""
    signature: str = ""
    nonce: int = 0
    
    def calculate_gas_cost(self) -> int:
        """Calculate gas cost."""
        return self.gas_used * self.gas_price
    
    def to_dict(self) -> Dict:
        """Convert transaction to dictionary."""
        return {
            "tx_id": self.tx_id,
            "from_address": self.from_address,
            "to_address": self.to_address,
            "amount": self.amount,
            "transaction_type": self.transaction_type.value,
            "timestamp": self.timestamp,
            "gas_limit": self.gas_limit,
            "gas_used": self.gas_used,
            "gas_price": self.gas_price,
            "data": self.data,
            "signature": self.signature,
            "nonce": self.nonce
        }


class MerkleTree:
    """Merkle tree implementation."""
    
    def __init__(self, data: List[str]):
        """Initialize Merkle tree."""
        self.data = data
        self.root = self._build_tree(data)
    
    def _build_tree(self, data: List[str]) -> Optional[MerkleNode]:
        """Build Merkle tree from data."""
        if not data:
            return None
        
        # Hash leaf nodes
        leaves = [MerkleNode(hashlib.sha256(item.encode()).hexdigest()) 
                 for item in data]
        
        # Build tree
        while len(leaves) > 1:
            new_level = []
            
            for i in range(0, len(leaves), 2):
                left = leaves[i]
                right = leaves[i + 1] if i + 1 < len(leaves) else left
                
                combined_hash = hashlib.sha256(
                    (left.hash + right.hash).encode()
                ).hexdigest()
                
                new_level.append(MerkleNode(combined_hash, left, right))
            
            leaves = new_level
        
        return leaves[0] if leaves else None
    
    def get_root_hash(self) -> str:
        """Get Merkle root hash."""
        return self.root.hash if self.root else ""
    
    def verify_proof(self, data: str, proof: List[Tuple[str, bool]]) -> bool:
        """Verify Merkle proof."""
        current_hash = hashlib.sha256(data.encode()).hexdigest()
        
        for proof_hash, is_left in proof:
            if is_left:
                current_hash = hashlib.sha256(
                    (proof_hash + current_hash).encode()
                ).hexdigest()
            else:
                current_hash = hashlib.sha256(
                    (current_hash + proof_hash).encode()
                ).hexdigest()
        
        return current_hash == self.get_root_hash()


class ConsensusAlgorithm:
    """Consensus algorithm implementations."""
    
    @staticmethod
    def proof_of_work(block_data: str, difficulty: int = 4) -> Tuple[str, int]:
        """Simple proof of work mining."""
        target = "0" * difficulty
        nonce = 0
        
        while True:
            data_to_hash = f"{block_data}{nonce}"
            hash_result = hashlib.sha256(data_to_hash.encode()).hexdigest()
            
            if hash_result.startswith(target):
                return hash_result, nonce
            
            nonce += 1
    
    @staticmethod
    def proof_of_stake(validators: Dict[str, int], seed: str) -> str:
        """Simple proof of stake selection."""
        total_stake = sum(validators.values())
        selection = int(hashlib.sha256(seed.encode()).hexdigest(), 16) % total_stake
        
        current = 0
        for validator, stake in validators.items():
            current += stake
            if current > selection:
                return validator
        
        return list(validators.keys())[0]


class GasCalculator:
    """Gas calculation utilities."""
    
    BASE_GAS_COST = 21000
    GAS_PER_BYTE = 20
    CONTRACT_CALL_GAS = 10000
    STORAGE_WRITE_GAS = 20000
    STORAGE_READ_GAS = 2000
    
    @staticmethod
    def calculate_transfer_gas(data_size: int = 0) -> int:
        """Calculate gas for transfer transaction."""
        gas = GasCalculator.BASE_GAS_COST
        gas += data_size * GasCalculator.GAS_PER_BYTE
        return gas
    
    @staticmethod
    def calculate_contract_call_gas(data_size: int = 0, 
                                   storage_writes: int = 0,
                                   storage_reads: int = 0) -> int:
        """Calculate gas for contract call."""
        gas = GasCalculator.CONTRACT_CALL_GAS
        gas += data_size * GasCalculator.GAS_PER_BYTE
        gas += storage_writes * GasCalculator.STORAGE_WRITE_GAS
        gas += storage_reads * GasCalculator.STORAGE_READ_GAS
        return gas


class StateManager:
    """Blockchain state management."""
    
    def __init__(self):
        """Initialize state manager."""
        self.accounts: Dict[str, Dict] = defaultdict(lambda: {
            "balance": 0,
            "nonce": 0,
            "storage": {},
            "code": None
        })
        self.contracts: Dict[str, SmartContract] = {}
    
    def get_balance(self, address: str) -> int:
        """Get account balance."""
        return self.accounts[address]["balance"]
    
    def set_balance(self, address: str, balance: int) -> None:
        """Set account balance."""
        self.accounts[address]["balance"] = balance
    
    def transfer(self, from_address: str, to_address: str, amount: int) -> bool:
        """Transfer balance between accounts."""
        if self.get_balance(from_address) >= amount:
            self.set_balance(from_address, self.get_balance(from_address) - amount)
            self.set_balance(to_address, self.get_balance(to_address) + amount)
            return True
        return False
    
    def deploy_contract(self, address: str, code: str, owner: str) -> str:
        """Deploy smart contract."""
        contract_address = hashlib.sha256(
            f"{address}{time.time()}".encode()
        ).hexdigest()[:40]
        
        contract = SmartContract(
            address=contract_address,
            code=code,
            storage={},
            owner=owner
        )
        
        self.contracts[contract_address] = contract
        return contract_address
    
    def call_contract(self, contract_address: str, function: str, 
                     args: List[Any]) -> Any:
        """Call smart contract function."""
        contract = self.contracts.get(contract_address)
        if contract:
            return contract.call(function, args)
        return None
    
    def get_contract_storage(self, contract_address: str, key: str) -> Any:
        """Get contract storage value."""
        contract = self.contracts.get(contract_address)
        if contract:
            return contract.get_storage(key)
        return None
    
    def set_contract_storage(self, contract_address: str, key: str, value: Any) -> None:
        """Set contract storage value."""
        contract = self.contracts.get(contract_address)
        if contract:
            contract.set_storage(key, value)


class TransactionProcessor:
    """Transaction processing utilities."""
    
    def __init__(self, state_manager: StateManager):
        """Initialize transaction processor."""
        self.state_manager = state_manager
        self.pending_transactions: List[Transaction] = []
        self.processed_transactions: List[Transaction] = []
    
    def add_transaction(self, transaction: Transaction) -> bool:
        """Add transaction to pending pool."""
        # Validate transaction
        if self._validate_transaction(transaction):
            self.pending_transactions.append(transaction)
            return True
        return False
    
    def _validate_transaction(self, transaction: Transaction) -> bool:
        """Validate transaction."""
        # Check balance
        if transaction.transaction_type == TransactionType.TRANSFER:
            balance = self.state_manager.get_balance(transaction.from_address)
            if balance < transaction.amount:
                return False
        
        # Check nonce (simplified)
        account_nonce = self.state_manager.accounts[transaction.from_address]["nonce"]
        if transaction.nonce < account_nonce:
            return False
        
        return True
    
    def process_transaction(self, transaction: Transaction) -> bool:
        """Process transaction."""
        try:
            if transaction.transaction_type == TransactionType.TRANSFER:
                success = self.state_manager.transfer(
                    transaction.from_address,
                    transaction.to_address,
                    transaction.amount
                )
                
                if success:
                    self.state_manager.accounts[transaction.from_address]["nonce"] += 1
                    transaction.gas_used = GasCalculator.calculate_transfer_gas()
                    self.processed_transactions.append(transaction)
                    return True
            
            elif transaction.transaction_type == TransactionType.CONTRACT_DEPLOY:
                contract_address = self.state_manager.deploy_contract(
                    transaction.from_address,
                    transaction.data,
                    transaction.from_address
                )
                
                transaction.gas_used = GasCalculator.calculate_contract_call_gas()
                self.processed_transactions.append(transaction)
                return True
            
            elif transaction.transaction_type == TransactionType.CONTRACT_CALL:
                result = self.state_manager.call_contract(
                    transaction.to_address,
                    "execute",
                    json.loads(transaction.data) if transaction.data else []
                )
                
                transaction.gas_used = GasCalculator.calculate_contract_call_gas()
                self.processed_transactions.append(transaction)
                return True
            
            return False
        except Exception as e:
            print(f"Transaction processing error: {e}")
            return False
    
    def process_pending_transactions(self, max_transactions: int = 10) -> int:
        """Process pending transactions."""
        processed = 0
        
        for transaction in self.pending_transactions[:max_transactions]:
            if self.process_transaction(transaction):
                self.pending_transactions.remove(transaction)
                processed += 1
        
        return processed


class Wallet:
    """Wallet management utilities."""
    
    def __init__(self):
        """Initialize wallet."""
        self.private_key: Optional[str] = None
        self.public_key: Optional[str] = None
        self.address: Optional[str] = None
    
    def generate_keypair(self) -> Tuple[str, str]:
        """Generate new keypair."""
        if ECDSA_AVAILABLE:
            # Use ecdsa library
            sk = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
            vk = sk.get_verifying_key()
            
            self.private_key = sk.to_string().hex()
            self.public_key = vk.to_string().hex()
            self.address = hashlib.sha256(self.public_key.encode()).hexdigest()[:40]
            
            return self.private_key, self.public_key
        else:
            # Fallback to simple generation
            import random
            self.private_key = hashlib.sha256(str(random.random()).encode()).hexdigest()
            self.public_key = hashlib.sha256(self.private_key.encode()).hexdigest()
            self.address = hashlib.sha256(self.public_key.encode()).hexdigest()[:40]
            
            return self.private_key, self.public_key
    
    def sign_transaction(self, transaction: Transaction) -> str:
        """Sign transaction with private key."""
        if not self.private_key:
            return ""
        
        # Create transaction hash
        tx_data = f"{transaction.from_address}{transaction.to_address}{transaction.amount}{transaction.nonce}"
        tx_hash = hashlib.sha256(tx_data.encode()).hexdigest()
        
        if ECDSA_AVAILABLE:
            # Sign with ecdsa
            sk = ecdsa.SigningKey.from_string(bytes.fromhex(self.private_key), curve=ecdsa.SECP256k1)
            signature = sk.sign(tx_hash.encode()).hex()
            return signature
        else:
            # Fallback
            return hashlib.sha256(f"{self.private_key}{tx_hash}".encode()).hexdigest()
    
    def verify_signature(self, transaction: Transaction, signature: str) -> bool:
        """Verify transaction signature."""
        if not self.public_key:
            return False
        
        tx_data = f"{transaction.from_address}{transaction.to_address}{transaction.amount}{transaction.nonce}"
        tx_hash = hashlib.sha256(tx_data.encode()).hexdigest()
        
        if ECDSA_AVAILABLE:
            try:
                vk = ecdsa.VerifyingKey.from_string(bytes.fromhex(self.public_key), curve=ecdsa.SECP256k1)
                return vk.verify(bytes.fromhex(signature), tx_hash.encode())
            except:
                return False
        else:
            # Fallback verification
            expected = hashlib.sha256(f"{self.private_key}{tx_hash}".encode()).hexdigest()
            return signature == expected


class BlockchainNetwork:
    """Blockchain networking concepts."""
    
    def __init__(self):
        """Initialize blockchain network."""
        self.nodes: Dict[str, Dict] = {}
        self.peers: List[str] = []
    
    def add_node(self, node_id: str, address: str, port: int) -> None:
        """Add node to network."""
        self.nodes[node_id] = {
            "address": address,
            "port": port,
            "last_seen": time.time(),
            "height": 0
        }
    
    def remove_node(self, node_id: str) -> bool:
        """Remove node from network."""
        if node_id in self.nodes:
            del self.nodes[node_id]
            return True
        return False
    
    def broadcast_transaction(self, transaction: Transaction) -> int:
        """Broadcast transaction to all peers."""
        # Simulated broadcast
        broadcast_count = len(self.peers)
        return broadcast_count
    
    def sync_blocks(self, node_id: str) -> bool:
        """Sync blocks with node."""
        # Simulated sync
        if node_id in self.nodes:
            return True
        return False
    
    def get_network_stats(self) -> Dict:
        """Get network statistics."""
        return {
            "total_nodes": len(self.nodes),
            "peers": len(self.peers),
            "active_nodes": sum(1 for node in self.nodes.values() 
                              if time.time() - node["last_seen"] < 300)
        }


class BlockValidator:
    """Block validation utilities."""
    
    @staticmethod
    def validate_block_hash(block_data: Dict, difficulty: int = 4) -> bool:
        """Validate block hash meets difficulty."""
        block_hash = block_data.get("hash", "")
        target = "0" * difficulty
        return block_hash.startswith(target)
    
    @staticmethod
    def validate_merkle_root(transactions: List[Transaction], merkle_root: str) -> bool:
        """Validate Merkle root."""
        tx_hashes = [tx.tx_id for tx in transactions]
        merkle_tree = MerkleTree(tx_hashes)
        calculated_root = merkle_tree.get_root_hash()
        return calculated_root == merkle_root
    
    @staticmethod
    def validate_transactions(transactions: List[Transaction], 
                             state_manager: StateManager) -> bool:
        """Validate all transactions in block."""
        for tx in transactions:
            # Check signature
            if not tx.signature:
                return False
            
            # Check nonce
            account_nonce = state_manager.accounts[tx.from_address]["nonce"]
            if tx.nonce != account_nonce:
                return False
        
        return True


class BlockchainAnalytics:
    """Blockchain analytics utilities."""
    
    @staticmethod
    def calculate_total_supply(state_manager: StateManager) -> int:
        """Calculate total token supply."""
        total = 0
        for address, account in state_manager.accounts.items():
            total += account["balance"]
        return total
    
    @staticmethod
    def get_top_holders(state_manager: StateManager, limit: int = 10) -> List[Tuple[str, int]]:
        """Get top token holders."""
        holders = [(addr, acc["balance"]) for addr, acc in state_manager.accounts.items()]
        holders.sort(key=lambda x: x[1], reverse=True)
        return holders[:limit]
    
    @staticmethod
    def calculate_transaction_volume(transactions: List[Transaction]) -> int:
        """Calculate total transaction volume."""
        return sum(tx.amount for tx in transactions if tx.transaction_type == TransactionType.TRANSFER)
    
    @staticmethod
    def calculate_gas_statistics(transactions: List[Transaction]) -> Dict:
        """Calculate gas statistics."""
        if not transactions:
            return {"avg_gas": 0, "total_gas": 0, "max_gas": 0}
        
        total_gas = sum(tx.gas_used for tx in transactions)
        avg_gas = total_gas / len(transactions)
        max_gas = max(tx.gas_used for tx in transactions)
        
        return {
            "avg_gas": avg_gas,
            "total_gas": total_gas,
            "max_gas": max_gas
        }


def demonstrate_blockchain_advanced():
    """Demonstrate advanced blockchain functionality."""
    print("=== Blockchain Advanced Demonstration ===\n")
    
    # Merkle Tree
    print("1. Merkle Tree:")
    data = ["tx1", "tx2", "tx3", "tx4"]
    merkle_tree = MerkleTree(data)
    print(f"   Root hash: {merkle_tree.get_root_hash()[:16]}...")
    
    # Consensus
    print("\n2. Consensus Algorithms:")
    hash_result, nonce = ConsensusAlgorithm.proof_of_work("test", difficulty=2)
    print(f"   PoW result: {hash_result[:16]}..., nonce: {nonce}")
    
    validators = {"validator1": 100, "validator2": 200, "validator3": 150}
    selected = ConsensusAlgorithm.proof_of_stake(validators, "seed123")
    print(f"   PoS selected: {selected}")
    
    # Smart Contract
    print("\n3. Smart Contract:")
    contract = SmartContract(
        address="0x123",
        code="function add(a, b) { return a + b; }",
        storage={},
        owner="0xabc"
    )
    result = contract.call("add", [5, 3])
    print(f"   Contract call result: {result}")
    
    contract.set_storage("key1", "value1")
    print(f"   Storage value: {contract.get_storage('key1')}")
    
    # State Management
    print("\n4. State Management:")
    state = StateManager()
    state.set_balance("0xalice", 1000)
    state.set_balance("0xbob", 500)
    
    print(f"   Alice balance: {state.get_balance('0xalice')}")
    print(f"   Bob balance: {state.get_balance('0xbob')}")
    
    success = state.transfer("0xalice", "0xbob", 100)
    print(f"   Transfer success: {success}")
    print(f"   Alice balance after: {state.get_balance('0xalice')}")
    print(f"   Bob balance after: {state.get_balance('0xbob')}")
    
    # Transaction Processing
    print("\n5. Transaction Processing:")
    processor = TransactionProcessor(state)
    
    tx = Transaction(
        tx_id="tx_001",
        from_address="0xalice",
        to_address="0xbob",
        amount=50,
        transaction_type=TransactionType.TRANSFER,
        timestamp=time.time(),
        nonce=1
    )
    
    processor.add_transaction(tx)
    processed = processor.process_pending_transactions()
    print(f"   Processed {processed} transactions")
    
    # Wallet
    print("\n6. Wallet:")
    wallet = Wallet()
    private_key, public_key = wallet.generate_keypair()
    print(f"   Address: {wallet.address[:16]}...")
    
    # Gas Calculation
    print("\n7. Gas Calculation:")
    transfer_gas = GasCalculator.calculate_transfer_gas(data_size=100)
    contract_gas = GasCalculator.calculate_contract_call_gas(
        data_size=50, storage_writes=2, storage_reads=1
    )
    print(f"   Transfer gas: {transfer_gas}")
    print(f"   Contract call gas: {contract_gas}")
    
    # Blockchain Network
    print("\n8. Blockchain Network:")
    network = BlockchainNetwork()
    network.add_node("node1", "192.168.1.1", 8000)
    network.add_node("node2", "192.168.1.2", 8000)
    
    stats = network.get_network_stats()
    print(f"   Network stats: {stats}")
    
    # Block Validation
    print("\n9. Block Validation:")
    block_data = {"hash": "0000abcdef123456"}
    valid = BlockValidator.validate_block_hash(block_data, difficulty=4)
    print(f"   Block hash valid: {valid}")
    
    # Analytics
    print("\n10. Blockchain Analytics:")
    total_supply = BlockchainAnalytics.calculate_total_supply(state)
    print(f"   Total supply: {total_supply}")
    
    top_holders = BlockchainAnalytics.get_top_holders(state, limit=3)
    print(f"   Top holders: {[(h[0][:8] + '...', h[1]) for h in top_holders]}")
    
    gas_stats = BlockchainAnalytics.calculate_gas_statistics(processor.processed_transactions)
    print(f"   Gas stats: {gas_stats}")
    
    print("\n=== Demonstration Complete ===")
    print("\nBlockchain Advanced Best Practices:")
    print("- Use proper cryptographic libraries for production")
    print("- Implement proper gas estimation for transactions")
    print("- Use Merkle trees for efficient verification")
    print("- Implement proper state management and persistence")
    print("- Use appropriate consensus for your use case")
    print("- Validate all transactions before processing")
    print("- Implement proper transaction ordering")
    print("- Use proper wallet security measures")
    print("- Monitor network health and performance")
    print("- Implement proper block validation")
    print("- Use appropriate difficulty adjustment")
    print("- Consider scalability solutions")
    print("- Implement proper replay protection")


if __name__ == "__main__":
    demonstrate_blockchain_advanced()
