# EquiExchange Frontend

A Next.js frontend for the EquiExchange decentralized trading platform, featuring wallet connection, automated negotiation, and blockchain recording.

## Features

- 🔗 **Wallet Connection**: MetaMask integration with Sepolia testnet
- 🤝 **Automated Negotiation**: AI-powered buyer/seller negotiation flow
- ⛓️ **Blockchain Recording**: Record agreements on Ethereum Sepolia testnet
- 🎨 **Modern UI**: Beautiful interface built with TailwindCSS
- 📱 **Responsive Design**: Works on desktop and mobile devices

## Tech Stack

- **Framework**: Next.js 14 with TypeScript
- **Wallet**: RainbowKit + wagmi + viem
- **Styling**: TailwindCSS
- **Icons**: Lucide React
- **HTTP Client**: Axios

## Getting Started

### Prerequisites

- Node.js 18+ 
- npm or yarn
- MetaMask wallet with Sepolia testnet configured
- Running EquiExchange backend API
- Deployed EquiExchangeRecords contract on Sepolia

### Installation

1. Install dependencies:
```bash
npm install
```

2. Copy environment variables:
```bash
cp env.example .env.local
```

3. Configure your environment variables in `.env.local`:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_CONTRACT_ADDRESS=0x... # Your deployed contract address
NEXT_PUBLIC_SEPOLIA_RPC_URL=https://sepolia.infura.io/v3/YOUR_PROJECT_ID
NEXT_PUBLIC_WALLET_CONNECT_PROJECT_ID=your-project-id
```

4. Run the development server:
```bash
npm run dev
```

5. Open [http://localhost:3000](http://localhost:3000) in your browser.

## Usage

1. **Connect Wallet**: Click the "Connect Wallet" button and connect your MetaMask wallet
2. **Start Negotiation**: Fill out the negotiation form with your trading parameters
3. **Run Negotiation**: Click "Run Negotiation" to start the automated negotiation process
4. **Record Agreement**: Once an agreement is reached, click "Record on Blockchain" to store it on Ethereum
5. **View Transaction**: Click the Etherscan link to view your transaction on the blockchain

## Project Structure

```
frontend/
├── app/
│   ├── globals.css          # Global styles
│   ├── layout.tsx           # Root layout
│   ├── page.tsx             # Home page
│   └── providers.tsx        # Wagmi/RainbowKit providers
├── components/
│   ├── AgreementDisplay.tsx # Agreement display and blockchain recording
│   ├── Header.tsx           # App header with wallet connection
│   ├── NegotiationForm.tsx  # Initial negotiation form
│   └── NegotiationFlow.tsx  # Negotiation timeline and controls
├── lib/
│   ├── api.ts               # Backend API client
│   ├── contract.ts          # Smart contract configuration
│   ├── utils.ts             # Utility functions
│   └── wagmi.ts             # Wagmi configuration
└── package.json
```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `NEXT_PUBLIC_API_URL` | Backend API URL | Yes |
| `NEXT_PUBLIC_CONTRACT_ADDRESS` | Deployed contract address | Yes |
| `NEXT_PUBLIC_SEPOLIA_RPC_URL` | Sepolia RPC endpoint | Yes |
| `NEXT_PUBLIC_WALLET_CONNECT_PROJECT_ID` | WalletConnect project ID | No |

## Smart Contract Integration

The frontend integrates with the `EquiExchangeRecords` smart contract:

- **recordAgreement()**: Records finalized agreements on the blockchain
- **getAgreement()**: Retrieves agreement details by hash
- **AgreementRecorded** event: Emitted when agreements are recorded

## Development

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint

### Adding New Features

1. Create components in the `components/` directory
2. Add API functions to `lib/api.ts`
3. Update contract configuration in `lib/contract.ts`
4. Add utility functions to `lib/utils.ts`

## Troubleshooting

### Common Issues

1. **Wallet not connecting**: Ensure MetaMask is installed and unlocked
2. **Transaction failing**: Check that you have Sepolia ETH for gas fees
3. **Contract not found**: Verify the contract address is correct and deployed
4. **API errors**: Ensure the backend is running and accessible

### Getting Sepolia ETH

1. Visit [Sepolia Faucet](https://sepoliafaucet.com/)
2. Enter your wallet address
3. Request test ETH (you'll need this for gas fees)

## License

MIT License - see LICENSE file for details.
