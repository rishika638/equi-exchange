# EquiExchange - Decentralized Trading Platform

A complete decentralized trading platform featuring AI-powered negotiations, smart contract integration, and blockchain recording. Built with Solidity, FastAPI, and Next.js.

## 🏗️ Project Architecture

```
equi_exchange/
├── contracts/          # Hardhat Solidity smart contracts
├── backend/           # FastAPI Python backend
└── frontend/          # Next.js React frontend
```

## 🚀 Features

### Smart Contracts (Solidity)
- **EquiExchangeRecords.sol**: Immutable agreement storage on Ethereum
- Agreement recording with hash verification
- Event emission for transparency

### Backend API (FastAPI)
- **Automated Negotiation Engine**: AI-powered buyer/seller negotiations
- **Session Management**: Create and manage trading sessions
- **Agreement Finalization**: Prepare agreements for blockchain recording
- **RESTful API**: Clean endpoints for frontend integration

### Frontend (Next.js + React)
- **Wallet Connection**: MetaMask integration with RainbowKit
- **Negotiation Room**: Real-time AI agent negotiations with 3-column layout
- **Blockchain Recording**: One-click agreement recording on Ethereum
- **Responsive Design**: Modern UI with TailwindCSS
- **Transaction Tracking**: Etherscan integration for transaction monitoring

## 📋 Prerequisites

- **Node.js** 18+ 
- **Python** 3.8+
- **MetaMask** wallet
- **Git**

## 🛠️ Installation & Setup

### 1. Clone Repository
```bash
git clone <your-repo-url>
cd equi_exchange
```

### 2. Smart Contracts Setup
```bash
cd contracts
npm install
npx hardhat compile
npx hardhat test
npx hardhat run scripts/deploy.js --network sepolia
```

### 3. Backend Setup
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000
```

### 4. Frontend Setup
```bash
cd frontend
npm install --legacy-peer-deps
cp env.example .env.local
# Edit .env.local with your configuration
npm run dev
```

## ⚙️ Environment Configuration

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_CONTRACT_ADDRESS=0x5FbDB2315678afecb367f032d93F642f64180aa3
NEXT_PUBLIC_SEPOLIA_RPC_URL=https://eth-sepolia.g.alchemy.com/v2/YOUR_ALCHEMY_KEY
NEXT_PUBLIC_ALCHEMY_KEY=your-alchemy-key
NEXT_PUBLIC_WALLET_CONNECT_PROJECT_ID=your-project-id
```

### Backend
```env
DATABASE_URL=sqlite:///./data.db
```

## 🎯 Usage Guide

### 1. Start All Services
```bash
# Terminal 1 - Backend
cd backend && python -m uvicorn app.main:app --reload

# Terminal 2 - Frontend  
cd frontend && npm run dev

# Terminal 3 - Contracts (if needed)
cd contracts && npx hardhat node
```

### 2. Access the Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### 3. Complete Trading Flow
1. **Connect Wallet**: Click "Connect Wallet" and connect MetaMask
2. **Start Negotiation**: Click "Run Auto-Negotiation" to begin AI negotiation
3. **Watch Timeline**: Observe real-time negotiation rounds with fairness scores
4. **View Agreement**: Click "View Final Agreement" to see results
5. **Record on Blockchain**: Click "Record on Blockchain" to store on Ethereum
6. **Verify Transaction**: Click Etherscan link to view on blockchain

## 🏛️ Smart Contract Details

### EquiExchangeRecords.sol
```solidity
contract EquiExchangeRecords {
    struct Agreement {
        bytes32 agreementHash;
        address partyA;
        address partyB;
        uint256 price;
        uint256 quantity;
        uint256 timestamp;
    }
    
    function recordAgreement(
        bytes32 _agreementHash,
        address _partyA,
        address _partyB,
        uint256 _price,
        uint256 _quantity
    ) public;
}
```

### Deployment
```bash
# Deploy to Sepolia
npx hardhat run scripts/deploy.js --network sepolia

# Verify contract
npx hardhat verify --network sepolia <CONTRACT_ADDRESS>
```

## 🔌 API Endpoints

### Sessions
- `POST /sessions` - Create new negotiation session
- `POST /sessions/{id}/auto` - Run automated negotiation
- `GET /sessions/{id}/timeline` - Get negotiation timeline
- `POST /sessions/{id}/finalize` - Finalize agreement

### Example API Usage
```javascript
// Create session
const session = await fetch('/sessions', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    role: 'buyer',
    buyer_address: '0x...',
    target_price: 85,
    min_price: 50,
    max_price: 100,
    quantity: 60
  })
});
```

## 🎨 Frontend Components

### Core Components
- **NegotiationRoom**: Main 3-column negotiation interface
- **AgentCard**: Reusable buyer/seller agent display
- **Timeline**: Real-time negotiation rounds with progress bars
- **FinalAgreement**: Agreement review and blockchain recording
- **Header**: Wallet connection and navigation

### Key Features
- **Real-time Updates**: Live negotiation progress
- **Responsive Design**: Mobile and desktop optimized
- **Error Handling**: Comprehensive error states
- **Loading States**: Smooth user experience
- **Transaction Tracking**: Complete blockchain integration

## 🔧 Development

### Available Scripts

#### Frontend
```bash
npm run dev          # Start development server
```

#### Backend
```bash
python -m uvicorn app.main:app --reload    # Development server
```

#### Contracts
```bash
npx hardhat compile    # Compile contracts
npx hardhat test       # Run tests
```

### Project Structure
```
frontend/
├── app/
│   ├── globals.css
│   ├── layout.tsx
│   ├── page.tsx
│   ├── providers.tsx
│   ├── negotiation-room/
│   └── final-agreement/
├── components/
│   ├── NegotiationRoom.tsx
│   ├── AgentCard.tsx
│   ├── Timeline.tsx
│   ├── FinalAgreement.tsx
│   └── ...
├── lib/
│   ├── api.ts
│   ├── contract.ts
│   ├── utils.ts
│   └── wagmi.ts
└── package.json

backend/
├── app/
│   ├── main.py
│   ├── routes.py
│   ├── models.py
│   ├── agents.py
│   └── utils.py
└── requirements.txt

contracts/
├── contracts/
│   └── EquiExchangeRecords.sol
├── scripts/
│   └── deploy.js
├── test/
└── hardhat.config.js
```

## 🔒 Security Considerations

- **Smart Contract**: Audited and tested on testnet
- **Wallet Integration**: Secure MetaMask connection
- **API Security**: Input validation and error handling
- **Environment Variables**: Sensitive data in .env files


## 📄 License

MIT License - see LICENSE file for details.

---

**Built by using Solidity, FastAPI, Next.js, and TailwindCSS**
