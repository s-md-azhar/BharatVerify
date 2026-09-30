import { useParams } from 'react-router-dom';
import { Check, AlertTriangle, X } from 'lucide-react';

export function CaseDetails() {
  const { id } = useParams();

  // Mock data for demonstration
  const status: string = 'REVIEW';
  
  return (
    <div className="space-y-6">
      {/* Header Banner */}
      <h1 className="text-xl font-bold text-slate-800">Case Details: {id}</h1>
      <div className={`p-4 rounded-lg flex items-center ${status === 'VERIFIED' ? 'bg-emerald-50 border border-emerald-200' : status === 'REVIEW' ? 'bg-amber-50 border border-amber-200' : 'bg-rose-50 border border-rose-200'}`}>
        {status === 'VERIFIED' && <Check className="text-emerald-600 mr-3" />}
        {status === 'REVIEW' && <AlertTriangle className="text-amber-600 mr-3" />}
        {status === 'MISMATCH' && <X className="text-rose-600 mr-3" />}
        <div>
          <h2 className={`font-bold ${status === 'VERIFIED' ? 'text-emerald-800' : status === 'REVIEW' ? 'text-amber-800' : 'text-rose-800'}`}>
            Status: {status}
          </h2>
          <p className="text-sm text-slate-600 mt-1">Manual review required due to name variation and address mismatch.</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Left Column: Evidence */}
        <div className="space-y-6">
          <div className="card p-6">
            <h3 className="font-semibold text-slate-800 mb-4 border-b pb-2">Document Evidence</h3>
            <div className="bg-slate-100 h-64 rounded flex items-center justify-center text-slate-400 border border-dashed border-slate-300">
              [Synthetic Document Image Preview]
            </div>
          </div>
          
          <div className="card p-6">
            <h3 className="font-semibold text-slate-800 mb-4 border-b pb-2">Face Verification</h3>
            <div className="flex space-x-4">
              <div className="flex-1 bg-slate-100 h-32 rounded flex items-center justify-center text-xs text-slate-400 border">
                Selfie
              </div>
              <div className="flex-1 bg-slate-100 h-32 rounded flex items-center justify-center text-xs text-slate-400 border">
                ID Photo
              </div>
            </div>
            <p className="mt-4 text-sm text-emerald-600 font-medium flex items-center">
              <Check className="w-4 h-4 mr-1" /> Match (Similarity: 0.89)
            </p>
          </div>
        </div>

        {/* Right Column: Fields Comparison */}
        <div className="card p-0 overflow-hidden">
          <div className="p-4 border-b border-slate-200 bg-slate-50">
            <h3 className="font-semibold text-slate-800">Field Comparison</h3>
          </div>
          <table className="min-w-full divide-y divide-slate-200">
            <thead className="bg-slate-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Field</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Application Data</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Extracted Data</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Match</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-slate-200 text-sm">
              <tr>
                <td className="px-6 py-4 font-medium text-slate-900">Name</td>
                <td className="px-6 py-4 text-slate-600">Rahul Sharma</td>
                <td className="px-6 py-4 text-slate-600">Rahul S Sharma</td>
                <td className="px-6 py-4"><span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-amber-100 text-amber-800">REVIEW</span></td>
              </tr>
              <tr>
                <td className="px-6 py-4 font-medium text-slate-900">DOB</td>
                <td className="px-6 py-4 text-slate-600">12/05/1990</td>
                <td className="px-6 py-4 text-slate-600">12/05/1990</td>
                <td className="px-6 py-4"><span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-emerald-100 text-emerald-800">MATCH</span></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
