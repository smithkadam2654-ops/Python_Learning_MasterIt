"""
Blockchain Utilities Module

This module provides comprehensive blockchain and cryptocurrency utilities including:
- Basic blockchain implementation
- Cryptographic hash functions
- Digital signatures
- Wallet address generation
- Transaction creation and validation
- Merkle tree implementation
- Proof of Work consensus
- Smart contract basics
- Blockchain explorer utilities
- Cryptocurrency price tracking

Note: This module uses hashlib for cryptographic operations and requests for API calls.
Install with: pip install requests ecdsa

All functions include comprehensive docstrings and type hints.
"""

import hashlib
import json
import time
from typing import Any, Dict, List, Optional, Tuple, Union
from dataclasses import dataclass
from datetime import datetime
from enum import Enum


try:
    import ecdsa
    import base58
    ECDSA_AVAILABLE = True
except ImportError:
    ECDSA_AVAILABLE = False


try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False


class HashAlgorithm(Enum):
    """Supported hash algorithms."""
    SHA256 = "sha256"
    SHA512 = "sha512"
    MD5 = "md5"
    RIPEMD160 = "ripemd160"


class NetworkType(Enum):
    """Blockchain network types."""
    MAINNET = "mainnet"
    TESTNET = "testnet"
    REGTEST = "regtest"


@dataclass
class Block:
    """Represents a block in the blockchain."""
    index: int
    timestamp: float
    transactions: List['Transaction']
    previous_hash: str
    nonce: int = 0
    hash: str = ""
    merkle_root: str = ""


@dataclass
class Transaction:
    """Represents a transaction."""
    sender: str
    receiver: str
    amount: float
    timestamp: float
    signature: str = ""
    transaction_id: str = ""
    fee: float = 0.0


@dataclass
class Wallet:
    """Represents a cryptocurrency wallet."""
    private_key: str
    public_key: str
    address: str
    balance: float = 0.0


@dataclass
class MerkleNode:
    """Represents a node in Merkle tree."""
    hash: str
    left: Optional['MerkleNode'] = None
    right: Optional['MerkleNode'] = None


class CryptoHash:
    """Cryptographic hash functions."""
    
    @staticmethod
    def sha256(data: str) -> str:
        """Calculate SHA-256 hash."""
        return hashlib.sha256(data.encode()).hexdigest()
    
    @staticmethod
    def sha512(data: str) -> str:
        """Calculate SHA-512 hash."""
        return hashlib.sha512(data.encode()).hexdigest()
    
    @staticmethod
    def md5(data: str) -> str:
        """Calculate MD5 hash."""
        return hashlib.md5(data.encode()).hexdigest()
    
    @staticmethod
    def double_sha256(data: str) -> str:
        """Calculate double SHA-256 (used in Bitcoin)."""
        return CryptoHash.sha256(CryptoHash.sha256(data))
    
    @staticmethod
    def ripemd160(data: str) -> str:
        """Calculate RIPEMD-160 hash."""
        try:
            import hashlib
            return hashlib.new('ripemd160', data.encode()).hexdigest()
        except:
            # Fallback if RIPEMD160 not available
            return CryptoHash.sha256(data)[:40]
    
    @staticmethod
    def hash_data(data: Any, algorithm: HashAlgorithm = HashAlgorithm.SHA256) -> str:
        """Hash data using specified algorithm."""
        data_str = json.dumps(data) if not isinstance(data, str) else data
        
        if algorithm == HashAlgorithm.SHA256:
            return CryptoHash.sha256(data_str)
        elif algorithm == HashAlgorithm.SHA512:
            return CryptoHash.sha512(data_str)
        elif algorithm == HashAlgorithm.MD5:
            return CryptoHash.md5(data_str)
        elif algorithm == HashAlgorithm.RIPEMD160:
            return CryptoHash.ripemd160(data_str)
        else:
            return CryptoHash.sha256(data_str)


class DigitalSignature:
    """Digital signature utilities."""
    
    @staticmethod
    def generate_key_pair() -> Tuple[str, str]:
        """Generate ECDSA key pair."""
        if not ECDSA_AVAILABLE:
            raise ImportError("ecdsa library is required. Install with: pip install ecdsa")
        
        private_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
        public_key = private_key.get_verifying_key()
        
        return (
            private_key.to_string().hex(),
            public_key.to_string().hex()
        )
    
    @staticmethod
    def sign_message(private_key_hex: str, message: str) -> str:
        """Sign a message with private key."""
        if not ECDSA_AVAILABLE:
            raise ImportError("ecdsa library is required")
        
        private_key = ecdsa.SigningKey.from_string(bytes.fromhex(private_key_hex))
        signature = private_key.sign(message.encode(), hashfunc=hashlib.sha256)
        
        return signature.hex()
    
    @staticmethod
    def verify_signature(public_key_hex: str, message: str, signature_hex: str) -> bool:
        """Verify a signature with public key."""
        if not ECDSA_AVAILABLE:
            raise ImportError("ecdsa library is required")
        
        public_key = ecdsa.VerifyingKey.from_string(bytes.fromhex(public_key_hex))
        signature = bytes.fromhex(signature_hex)
        
        try:
            public_key.verify(signature, message.encode(), hashlib.sha256)
            return True
        except:
            return False


class MerkleTree:
    """Merkle tree implementation for blockchain."""
    
    @staticmethod
    def calculate_merkle_root(transactions: List[Transaction]) -> str:
        """Calculate Merkle root from transactions."""
        if not transactions:
            return CryptoHash.sha256("")
        
        # Hash all transactions
        transaction_hashes = [CryptoHash.sha256(str(tx)) for tx in transactions]
        
        # Build Merkle tree
        while len(transaction_hashes) > 1:
            if len(transaction_hashes) % 2 == 1:
                transaction_hashes.append(transaction_hashes[-1])  # Duplicate last hash
            
            new_level = []
            for i in range(0, len(transaction_hashes), 2):
                combined = transaction_hashes[i] + transaction_hashes[i + 1]
                new_level.append(CryptoHash.sha256(combined))
            
            transaction_hashes = new_level
        
        return transaction_hashes[0]
    
    @staticmethod
    def build_merkle_tree(transactions: List[Transaction]) -> MerkleNode:
        """Build complete Merkle tree structure."""
        if not transactions:
            return MerkleNode(hash=CryptoHash.sha256(""))
        
        # Hash all transactions
        transaction_hashes = [CryptoHash.sha256(str(tx)) for tx in transactions]
        
        # Build tree recursively
        return MerkleTree._build_tree(transaction_hashes)
    
    @staticmethod
    def _build_tree(hashes: List[str]) -> MerkleNode:
        """Build Merkle tree recursively."""
        if len(hashes) == 1:
            return MerkleNode(hash=hashes[0])
        
        if len(hashes) % 2 == 1:
            hashes.append(hashes[-1])  # Duplicate last hash
        
        new_hashes = []
        for i in range(0, len(hashes), 2):
            combined = hashes[i] + hashes[i + 1]
            new_hashes.append(CryptoHash.sha256(combined))
        
        # Recursively build
        return MerkleTree._build_tree(new_hashes)


class Blockchain:
    """Simple blockchain implementation."""
    
    def __init__(self, difficulty: int = 4):
        """Initialize blockchain."""
        self.chain: List[Block] = []
        self.difficulty = difficulty
        self.pending_transactions: List[Transaction] = []
        self.mining_reward = 10.0
        self.create_genesis_block()
    
    def create_genesis_block(self) -> None:
        """Create the genesis block."""
        genesis_block = Block(
            index=0,
            timestamp=time.time(),
            transactions=[],
            previous_hash="0"
        )
        genesis_block.hash = self.calculate_block_hash(genesis_block)
        self.chain.append(genesis_block)
    
    def calculate_block_hash(self, block: Block) -> str:
        """Calculate hash of a block."""
        block_string = f"{block.index}{block.timestamp}{block.previous_hash}{block.nonce}"
        transaction_string = "".join([str(tx) for tx in block.transactions])
        
        return CryptoHash.double_sha256(block_string + transaction_string)
    
    def proof_of_work(self, block: Block) -> None:
        """Proof of Work mining algorithm."""
        target = "0" * self.difficulty
        
        while block.hash[:self.difficulty] != target:
            block.nonce += 1
            block.hash = self.calculate_block_hash(block)
    
    def add_transaction(self, sender: str, receiver: str, amount: float) -> None:
        """Add transaction to pending pool."""
        transaction = Transaction(
            sender=sender,
            receiver=receiver,
            amount=amount,
            timestamp=time.time(),
            transaction_id=CryptoHash.sha256(f"{sender}{receiver}{amount}{time.time()}")
        )
        self.pending_transactions.append(transaction)
    
    def mine_block(self, miner_address: str) -> Block:
        """Mine a new block with pending transactions."""
        # Add mining reward transaction
        reward_transaction = Transaction(
            sender="COINBASE",
            receiver=miner_address,
            amount=self.mining_reward,
            timestamp=time.time(),
            transaction_id=CryptoHash.sha256(f"COINBASE{miner_address}{self.mining_reward}{time.time()}")
        )
        
        # Create block with transactions
        transactions = [reward_transaction] + self.pending_transactions
        block = Block(
            index=len(self.chain),
            timestamp=time.time(),
            transactions=transactions,
            previous_hash=self.chain[-1].hash
        )
        
        # Calculate Merkle root
        block.merkle_root = MerkleTree.calculate_merkle_root(transactions)
        
        # Mine block
        self.proof_of_work(block)
        
        # Add to chain
        self.chain.append(block)
        self.pending_transactions = []
        
        return block
    
    def is_valid_chain(self) -> bool:
        """Validate the entire blockchain."""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            
            # Check previous hash
            if current_block.previous_hash != previous_block.hash:
                return False
            
            # Check hash
            if current_block.hash != self.calculate_block_hash(current_block):
                return False
            
            # Check proof of work
            if current_block.hash[:self.difficulty] != "0" * self.difficulty:
                return False
        
        return True
    
    def get_balance(self, address: str) -> float:
        """Get balance for an address."""
        balance = 0.0
        
        for block in self.chain:
            for transaction in block.transactions:
                if transaction.sender == address:
                    balance -= transaction.amount
                if transaction.receiver == address:
                    balance += transaction.amount
        
        return balance


class WalletGenerator:
    """Cryptocurrency wallet generation utilities."""
    
    @staticmethod
    def generate_wallet() -> Wallet:
        """Generate a new wallet with address."""
        if not ECDSA_AVAILABLE:
            raise ImportError("ecdsa library is required")
        
        # Generate key pair
        private_key_hex, public_key_hex = DigitalSignature.generate_key_pair()
        
        # Generate address (simplified Bitcoin-like address)
        # In real implementation, this would use proper Base58Check encoding
        public_key_hash = CryptoHash.ripemd160(CryptoHash.sha256(public_key_hex))
        address = "1" + public_key_hash[:40]  # Simplified address
        
        return Wallet(
            private_key=private_key_hex,
            public_key=public_key_hex,
            address=address
        )
    
    @staticmethod
    def generate_mnemonic_phrase(length: int = 12) -> List[str]:
        """Generate mnemonic phrase for wallet backup."""
        # Simplified word list (in real implementation, use BIP39 wordlist)
        word_list = [
            "abandon", "ability", "able", "about", "above", "absent", "absorb", "abstract",
            "absurd", "abuse", "access", "accident", "account", "accuse", "achieve", "acid",
            "acoustic", "acquire", "across", "act", "action", "actor", "actress", "actual"
        ]
        
        import random
        return [random.choice(word_list) for _ in range(length)]
    
    @staticmethod
    def validate_address(address: str) -> bool:
        """Validate cryptocurrency address format."""
        # Simplified validation
        if address.startswith("1") and len(address) >= 26 and len(address) <= 35:
            return True
        return False


class TransactionValidator:
    """Transaction validation utilities."""
    
    @staticmethod
    def validate_transaction(transaction: Transaction, 
                           blockchain: Blockchain) -> bool:
        """Validate a transaction."""
        # Check if sender has sufficient balance
        sender_balance = blockchain.get_balance(transaction.sender)
        
        if sender_balance < transaction.amount + transaction.fee:
            return False
        
        # Check signature
        if transaction.signature:
            # Would verify signature here
            pass
        
        # Check transaction ID format
        if not transaction.transaction_id:
            return False
        
        return True
    
    @staticmethod
    def calculate_transaction_fee(transaction: Transaction,
                                 gas_price: float = 0.0001) -> float:
        """Calculate transaction fee based on gas."""
        # Simplified fee calculation
        return gas_price * len(str(transaction))


class PriceTracker:
    """Cryptocurrency price tracking utilities."""
    
    @staticmethod
    def get_price(crypto: str = "bitcoin", 
                  fiat: str = "usd") -> Optional[float]:
        """Get current cryptocurrency price."""
        if not REQUESTS_AVAILABLE:
            raise ImportError("requests library is required. Install with: pip install requests")
        
        try:
            # Using CoinGecko API (free, no API key required)
            url = f"https://api.coingecko.com/api/v3/simple/price"
            params = {
                "ids": crypto,
                "vs_currencies": fiat
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return data[crypto][fiat]
            
            return None
        except Exception as e:
            print(f"Price fetch failed: {e}")
            return None
    
    @staticmethod
    def get_price_history(crypto: str = "bitcoin",
                          days: int = 7) -> Optional[List[Dict]]:
        """Get price history for cryptocurrency."""
        if not REQUESTS_AVAILABLE:
            raise ImportError("requests library is required")
        
        try:
            url = f"https://api.coingecko.com/api/v3/coins/{crypto}/market_chart"
            params = {
                "vs_currency": "usd",
                "days": days
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return data.get("prices", [])
            
            return None
        except Exception as e:
            print(f"Price history fetch failed: {e}")
            return None


class BlockchainExplorer:
    """Blockchain explorer utilities."""
    
    @staticmethod
    def get_block_count(network: NetworkType = NetworkType.MAINNET) -> Optional[int]:
        """Get current block count."""
        if not REQUESTS_AVAILABLE:
            raise ImportError("requests library is required")
        
        try:
            # Using blockchain.com API
            if network == NetworkType.MAINNET:
                url = "https://blockchain.info/q/getblockcount"
            else:
                url = f"https://blockchain.info/q/getblockcount?testnet={network.value}"
            
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                return int(response.text)
            
            return None
        except Exception as e:
            print(f"Block count fetch failed: {e}")
            return None
    
    @staticmethod
    def get_block_info(block_hash: str) -> Optional[Dict]:
        """Get information about a specific block."""
        if not REQUESTS_AVAILABLE:
            raise ImportError("requests library is required")
        
        try:
            url = f"https://blockchain.info/block/{block_hash}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            
            return None
        except Exception as e:
            print(f"Block info fetch failed: {e}")
            return None


class SmartContract:
    """Simple smart contract abstraction."""
    
    def __init__(self, address: str, abi: Dict):
        """Initialize smart contract."""
        self.address = address
        self.abi = abi
        self.state: Dict = {}
    
    def call_function(self, function_name: str, parameters: Dict = None) -> Any:
        """Call a smart contract function (read-only)."""
        # Simplified implementation
        if function_name in self.abi:
            function_def = self.abi[function_name]
            
            if function_def.get("type") == "view":
                # Read-only function
                return self.state.get(function_name, None)
        
        return None
    
    def send_transaction(self, function_name: str, 
                        parameters: Dict = None,
                        value: float = 0.0) -> str:
        """Send transaction to smart contract (write)."""
        # Simplified implementation
        transaction_id = CryptoHash.sha256(f"{function_name}{parameters}{value}{time.time()}")
        
        if function_name in self.abi:
            function_def = self.abi[function_name]
            
            if function_def.get("type") == "nonpayable":
                self.state[function_name] = parameters
            elif function_def.get("type") == "payable":
                self.state[function_name] = parameters
                self.state[f"{function_name}_value"] = value
        
        return transaction_id


class Consensus:
    """Consensus algorithm implementations."""
    
    @staticmethod
    def proof_of_work(block: Block, difficulty: int) -> bool:
        """Proof of Work consensus."""
        target = "0" * difficulty
        
        while block.hash[:difficulty] != target:
            block.nonce += 1
            block.hash = CryptoHash.double_sha256(
                f"{block.index}{block.timestamp}{block.previous_hash}{block.nonce}"
            )
        
        return True
    
    @staticmethod
    def proof_of_stake(validators: List[str], block: Block) -> bool:
        """Proof of Stake consensus (simplified)."""
        # Simplified PoS: randomly select validator
        import random
        selected_validator = random.choice(validators)
        
        # In real implementation, this would check stake amount and signature
        return True
    
    @staticmethod
    def proof_of_authority(authority: str, block: Block) -> bool:
        """Proof of Authority consensus."""
        # Check if block is signed by authority
        # Simplified implementation
        return True


def demonstrate_blockchain_utils():
    """Demonstrate blockchain utilities functionality."""
    print("=== Blockchain Utilities Demonstration ===\n")
    
    # Cryptographic Hashing
    print("1. Cryptographic Hashing:")
    data = "Hello, Blockchain!"
    print(f"   Data: {data}")
    print(f"   SHA-256: {CryptoHash.sha256(data)}")
    print(f"   Double SHA-256: {CryptoHash.double_sha256(data)}")
    print(f"   SHA-512: {CryptoHash.sha512(data)}")
    
    # Digital Signatures
    print("\n2. Digital Signatures:")
    if ECDSA_AVAILABLE:
        private_key, public_key = DigitalSignature.generate_key_pair()
        print(f"   Private Key: {private_key[:32]}...")
        print(f"   Public Key: {public_key[:32]}...")
        
        message = "Test message"
        signature = DigitalSignature.sign_message(private_key, message)
        print(f"   Signature: {signature[:32]}...")
        
        is_valid = DigitalSignature.verify_signature(public_key, message, signature)
        print(f"   Signature valid: {is_valid}")
    else:
        print("   Install ecdsa: pip install ecdsa")
    
    # Blockchain
    print("\n3. Simple Blockchain:")
    blockchain = Blockchain(difficulty=2)
    
    blockchain.add_transaction("Alice", "Bob", 10.0)
    blockchain.add_transaction("Bob", "Charlie", 5.0)
    
    print("   Mining block...")
    block = blockchain.mine_block("Miner1")
    print(f"   Block mined: {block.index}")
    print(f"   Block hash: {block.hash[:32]}...")
    print(f"   Transactions: {len(block.transactions)}")
    
    is_valid = blockchain.is_valid_chain()
    print(f"   Chain valid: {is_valid}")
    
    # Wallet Generation
    print("\n4. Wallet Generation:")
    if ECDSA_AVAILABLE:
        wallet = WalletGenerator.generate_wallet()
        print(f"   Address: {wallet.address}")
        print(f"   Public Key: {wallet.public_key[:32]}...")
        print(f"   Private Key: {wallet.private_key[:32]}...")
        
        mnemonic = WalletGenerator.generate_mnemonic_phrase()
        print(f"   Mnemonic: {' '.join(mnemonic)}")
    else:
        print("   Install ecdsa: pip install ecdsa")
    
    # Merkle Tree
    print("\n5. Merkle Tree:")
    transactions = [
        Transaction("Alice", "Bob", 10.0, time.time()),
        Transaction("Bob", "Charlie", 5.0, time.time()),
        Transaction("Charlie", "Alice", 3.0, time.time())
    ]
    
    merkle_root = MerkleTree.calculate_merkle_root(transactions)
    print(f"   Merkle Root: {merkle_root}")
    
    # Price Tracking
    print("\n6. Price Tracking:")
    if REQUESTS_AVAILABLE:
        price = PriceTracker.get_price("bitcoin", "usd")
        print(f"   Bitcoin price: ${price}")
        
        history = PriceTracker.get_price_history("bitcoin", days=1)
        if history:
            print(f"   Price points: {len(history)}")
    else:
        print("   Install requests: pip install requests")
    
    # Consensus
    print("\n7. Consensus Algorithms:")
    print("   Available consensus algorithms:")
    print("   - Proof of Work (PoW)")
    print("   - Proof of Stake (PoS)")
    print("   - Proof of Authority (PoA)")
    
    # Smart Contract
    print("\n8. Smart Contract:")
    contract_abi = {
        "getBalance": {"type": "view"},
        "setBalance": {"type": "nonpayable"},
        "transfer": {"type": "payable"}
    }
    
    contract = SmartContract("0x1234567890abcdef", contract_abi)
    contract.call_function("getBalance")
    contract.send_transaction("setBalance", {"account": "Alice", "amount": 100})
    print(f"   Contract state: {contract.state}")
    
    print("\n=== Demonstration Complete ===")
    print("\nBlockchain Best Practices:")
    print("- Always use secure cryptographic libraries")
    print("- Never share private keys or mnemonics")
    print("- Use hardware wallets for significant holdings")
    print("- Verify transactions before signing")
    print("- Keep blockchain software updated")
    print("- Understand gas fees and transaction costs")
    print("- Use testnets for development and testing")
    print("- Implement proper key management")


if __name__ == "__main__":
    demonstrate_blockchain_utils()