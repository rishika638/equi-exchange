'use client';

import { useState, useEffect } from 'react';
import { api, Offer } from '@/lib/api';
import { formatAddress } from '@/lib/utils';
import { ArrowLeft, Play, RefreshCw, CheckCircle } from 'lucide-react';

interface NegotiationFlowProps {
  sessionId: number;
  address: string;
  onAgreementReached: (agreement: any) => void;
  onNewNegotiation: () => void;
}

export function NegotiationFlow({ sessionId, address, onAgreementReached, onNewNegotiation }: NegotiationFlowProps) {
  const [offers, setOffers] = useState<Offer[]>([]);
  const [isRunning, setIsRunning] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [agreement, setAgreement] = useState<any>(null);

  const runNegotiation = async () => {
    setIsRunning(true);
    setIsLoading(true);
    
    try {
      const result = await api.runAutoNegotiation(sessionId);
      setAgreement(result.agreement);
      
      // Fetch the timeline to show offers
      const timelineResult = await api.getTimeline(sessionId);
      setOffers(timelineResult.offers);
      
      // Finalize the agreement
      const finalizedAgreement = await api.finalizeAgreement(sessionId);
      onAgreementReached(finalizedAgreement);
    } catch (error) {
      console.error('Error running negotiation:', error);
      alert('Failed to run negotiation');
    } finally {
      setIsLoading(false);
      setIsRunning(false);
    }
  };

  const loadTimeline = async () => {
    try {
      const result = await api.getTimeline(sessionId);
      setOffers(result.offers);
    } catch (error) {
      console.error('Error loading timeline:', error);
    }
  };

  useEffect(() => {
    loadTimeline();
  }, [sessionId]);

  return (
    <div className="max-w-4xl mx-auto">
      <div className="flex items-center justify-between mb-6">
        <button
          onClick={onNewNegotiation}
          className="flex items-center space-x-2 text-gray-600 hover:text-gray-800"
        >
          <ArrowLeft className="h-4 w-4" />
          <span>New Negotiation</span>
        </button>
        
        <div className="text-sm text-gray-600">
          Session ID: {sessionId}
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Control Panel */}
        <div className="lg:col-span-1">
          <div className="card">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              Negotiation Control
            </h3>
            
            <div className="space-y-4">
              <button
                onClick={runNegotiation}
                disabled={isLoading || isRunning}
                className="w-full btn-primary flex items-center justify-center space-x-2 disabled:opacity-50"
              >
                {isLoading ? (
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                ) : (
                  <>
                    <Play className="h-4 w-4" />
                    <span>Run Negotiation</span>
                  </>
                )}
              </button>
              
              <button
                onClick={loadTimeline}
                disabled={isLoading}
                className="w-full btn-secondary flex items-center justify-center space-x-2 disabled:opacity-50"
              >
                <RefreshCw className="h-4 w-4" />
                <span>Refresh Timeline</span>
              </button>
            </div>

            {agreement && (
              <div className="mt-6 p-4 bg-green-50 border border-green-200 rounded-lg">
                <div className="flex items-center space-x-2 text-green-800">
                  <CheckCircle className="h-5 w-5" />
                  <span className="font-medium">Agreement Reached!</span>
                </div>
                <div className="mt-2 text-sm text-green-700">
                  <p>Price: ${agreement.price}</p>
                  <p>Quantity: {agreement.quantity}</p>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Timeline */}
        <div className="lg:col-span-2">
          <div className="card">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              Negotiation Timeline
            </h3>
            
            {offers.length === 0 ? (
              <div className="text-center py-8 text-gray-500">
                <p>No offers yet. Click "Run Negotiation" to start.</p>
              </div>
            ) : (
              <div className="space-y-4">
                {offers.map((offer, index) => (
                  <div
                    key={index}
                    className={`p-4 rounded-lg border ${
                      offer.made_by === 'buyer'
                        ? 'bg-blue-50 border-blue-200'
                        : 'bg-green-50 border-green-200'
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-2">
                        <div className={`w-2 h-2 rounded-full ${
                          offer.made_by === 'buyer' ? 'bg-blue-500' : 'bg-green-500'
                        }`} />
                        <span className="font-medium text-gray-900">
                          {offer.made_by === 'buyer' ? 'Buyer' : 'Seller'}
                        </span>
                        <span className="text-sm text-gray-500">
                          Round {offer.round}
                        </span>
                      </div>
                      <div className="text-right">
                        <div className="text-lg font-semibold text-gray-900">
                          ${offer.price}
                        </div>
                        <div className="text-sm text-gray-500">
                          Qty: {offer.quantity}
                        </div>
                      </div>
                    </div>
                    
                    <div className="mt-2 grid grid-cols-2 gap-4 text-sm">
                      <div>
                        <span className="text-gray-500">Fairness:</span>
                        <span className="ml-2 font-medium">
                          {(offer.fairness * 100).toFixed(1)}%
                        </span>
                      </div>
                      <div>
                        <span className="text-gray-500">Utility:</span>
                        <span className="ml-2 font-medium">
                          {offer.utility.toFixed(2)}
                        </span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
