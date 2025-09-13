'use client';

import { useState } from 'react';
import { api, SessionData } from '@/lib/api';
import { formatAddress } from '@/lib/utils';
import { ArrowRight, User, DollarSign, Package } from 'lucide-react';

interface NegotiationFormProps {
  address: string;
  onSessionCreated: (session: any) => void;
}

export function NegotiationForm({ address, onSessionCreated }: NegotiationFormProps) {
  const [formData, setFormData] = useState<SessionData>({
    role: 'buyer',
    buyer_address: address,
    target_price: 75,
    min_price: 50,
    max_price: 100,
    quantity: 1,
    fairness_weight: 0.5,
    max_rounds: 8,
  });
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    
    try {
      const session = await api.createSession(formData);
      onSessionCreated(session);
    } catch (error) {
      console.error('Error creating session:', error);
      alert('Failed to create negotiation session');
    } finally {
      setIsLoading(false);
    }
  };

  const handleInputChange = (field: keyof SessionData, value: any) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  return (
    <div className="max-w-2xl mx-auto">
      <div className="card">
        <div className="text-center mb-6">
          <h2 className="text-2xl font-bold text-gray-900 mb-2">
            Start New Negotiation
          </h2>
          <p className="text-gray-600">
            Configure your trading parameters and start negotiating
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Role Selection */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Your Role
            </label>
            <div className="flex space-x-4">
              <label className="flex items-center">
                <input
                  type="radio"
                  value="buyer"
                  checked={formData.role === 'buyer'}
                  onChange={(e) => handleInputChange('role', e.target.value)}
                  className="mr-2"
                />
                <span className="flex items-center">
                  <User className="h-4 w-4 mr-1" />
                  Buyer
                </span>
              </label>
              <label className="flex items-center">
                <input
                  type="radio"
                  value="seller"
                  checked={formData.role === 'seller'}
                  onChange={(e) => handleInputChange('role', e.target.value)}
                  className="mr-2"
                />
                <span className="flex items-center">
                  <Package className="h-4 w-4 mr-1" />
                  Seller
                </span>
              </label>
            </div>
          </div>

          {/* Address Display */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Your Address
            </label>
            <div className="input-field bg-gray-50">
              {formatAddress(address)}
            </div>
          </div>

          {/* Price Range */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Target Price
              </label>
              <div className="relative">
                <DollarSign className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
                <input
                  type="number"
                  value={formData.target_price}
                  onChange={(e) => handleInputChange('target_price', parseFloat(e.target.value))}
                  className="input-field pl-10"
                  placeholder="75"
                />
              </div>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Min Price
              </label>
              <div className="relative">
                <DollarSign className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
                <input
                  type="number"
                  value={formData.min_price}
                  onChange={(e) => handleInputChange('min_price', parseFloat(e.target.value))}
                  className="input-field pl-10"
                  placeholder="50"
                />
              </div>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Max Price
              </label>
              <div className="relative">
                <DollarSign className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
                <input
                  type="number"
                  value={formData.max_price}
                  onChange={(e) => handleInputChange('max_price', parseFloat(e.target.value))}
                  className="input-field pl-10"
                  placeholder="100"
                />
              </div>
            </div>
          </div>

          {/* Quantity */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Quantity
            </label>
            <input
              type="number"
              value={formData.quantity}
              onChange={(e) => handleInputChange('quantity', parseInt(e.target.value))}
              className="input-field"
              placeholder="1"
              min="1"
            />
          </div>

          {/* Fairness Weight */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Fairness Weight: {formData.fairness_weight}
            </label>
            <input
              type="range"
              min="0"
              max="1"
              step="0.1"
              value={formData.fairness_weight}
              onChange={(e) => handleInputChange('fairness_weight', parseFloat(e.target.value))}
              className="w-full"
            />
            <div className="flex justify-between text-xs text-gray-500 mt-1">
              <span>Selfish (0)</span>
              <span>Fair (0.5)</span>
              <span>Altruistic (1)</span>
            </div>
          </div>

          {/* Max Rounds */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Max Negotiation Rounds
            </label>
            <input
              type="number"
              value={formData.max_rounds}
              onChange={(e) => handleInputChange('max_rounds', parseInt(e.target.value))}
              className="input-field"
              placeholder="8"
              min="1"
              max="20"
            />
          </div>

          <button
            type="submit"
            disabled={isLoading}
            className="w-full btn-primary flex items-center justify-center space-x-2 disabled:opacity-50"
          >
            {isLoading ? (
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
            ) : (
              <>
                <span>Start Negotiation</span>
                <ArrowRight className="h-4 w-4" />
              </>
            )}
          </button>
        </form>
      </div>
    </div>
  );
}
