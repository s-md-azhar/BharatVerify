import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

export function NewVerification() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    // Simulate API call
    setTimeout(() => {
      setLoading(false);
      navigate('/cases/demo-123'); // navigate to case details
    }, 1000);
  };

  return (
    <div className="max-w-2xl mx-auto card p-8">
      <h2 className="text-lg font-semibold text-slate-900 mb-6">Create Verification Case</h2>
      
      <form onSubmit={handleSubmit} className="space-y-5">
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">Applicant Name</label>
            <input type="text" required className="input-field" placeholder="Full legal name" />
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">Date of Birth</label>
            <input type="text" required className="input-field" placeholder="DD/MM/YYYY" />
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1">Address</label>
          <textarea rows={3} className="input-field" placeholder="Full address"></textarea>
        </div>

        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1">Upload Document (OVD)</label>
          <div className="mt-1 flex justify-center px-6 pt-5 pb-6 border-2 border-slate-300 border-dashed rounded-md">
            <div className="space-y-1 text-center">
              <div className="flex text-sm text-slate-600">
                <label className="relative cursor-pointer bg-white rounded-md font-medium text-primary-600 hover:text-primary-500 focus-within:outline-none focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-primary-500">
                  <span>Upload a file</span>
                  <input type="file" className="sr-only" />
                </label>
                <p className="pl-1">or drag and drop</p>
              </div>
              <p className="text-xs text-slate-500">PNG, JPG, PDF up to 10MB</p>
            </div>
          </div>
        </div>

        <div className="pt-4 flex justify-end">
          <button type="submit" disabled={loading} className="btn-primary w-full sm:w-auto">
            {loading ? 'Processing...' : 'Start Verification'}
          </button>
        </div>
      </form>
    </div>
  );
}
