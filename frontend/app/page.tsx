'use client';

import { useState } from 'react';
import { useAccount } from 'wagmi';
import { ConnectButton } from '@rainbow-me/rainbowkit';
import { Header } from '@/components/Header';
import { NegotiationForm } from '@/components/NegotiationForm';
import { NegotiationFlow } from '@/components/NegotiationFlow';
import { AgreementDisplay } from '@/components/AgreementDisplay';

export default function Home() {
  const { isConnected, address } = useAccount();
  const [sessionId, setSessionId] = useState<number | null>(null);
  const [agreement, setAgreement] = useState<any>(null);
  const [currentStep, setCurrentStep] = useState<'form' | 'negotiation' | 'agreement'>('form');

  const handleSessionCreated = (session: any) => {
    setSessionId(session.session_id);
    setCurrentStep('negotiation');
  };

  const handleAgreementReached = (agreementData: any) => {
    setAgreement(agreementData);
    setCurrentStep('agreement');
  };

  const handleNewNegotiation = () => {
    setSessionId(null);
    setAgreement(null);
    setCurrentStep('form');
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      
      <main className="container mx-auto px-4 py-8">
        {!isConnected ? (
          <div className="max-w-md mx-auto text-center">
            <div className="card">
              <h1 className="text-2xl font-bold text-gray-900 mb-4">
                Welcome to EquiExchange
              </h1>
              <p className="text-gray-600 mb-6">
                Connect your wallet to start trading on the decentralized exchange
              </p>
              <ConnectButton />
            </div>
          </div>
        ) : (
          <div className="max-w-4xl mx-auto">
            {currentStep === 'form' && (
              <NegotiationForm 
                address={address!}
                onSessionCreated={handleSessionCreated}
              />
            )}
            
            {currentStep === 'negotiation' && sessionId && (
              <NegotiationFlow 
                sessionId={sessionId}
                address={address!}
                onAgreementReached={handleAgreementReached}
                onNewNegotiation={handleNewNegotiation}
              />
            )}
            
            {currentStep === 'agreement' && agreement && (
              <AgreementDisplay 
                agreement={agreement}
                address={address!}
                onNewNegotiation={handleNewNegotiation}
              />
            )}
          </div>
        )}
      </main>
    </div>
  );
}
