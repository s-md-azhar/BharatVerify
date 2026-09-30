export function Evaluation() {
  return (
    <div className="space-y-6">
      <h2 className="text-lg font-semibold text-slate-900">Model Evaluation Metrics</h2>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="card p-6">
          <p className="text-sm text-slate-500 mb-1">Accuracy</p>
          <p className="text-3xl font-bold text-slate-900">94.2%</p>
        </div>
        <div className="card p-6">
          <p className="text-sm text-slate-500 mb-1">F1 Score</p>
          <p className="text-3xl font-bold text-slate-900">93.8%</p>
        </div>
        <div className="card p-6">
          <p className="text-sm text-slate-500 mb-1">Precision</p>
          <p className="text-3xl font-bold text-slate-900">95.1%</p>
        </div>
      </div>
      
      <div className="card p-6">
        <h3 className="text-md font-semibold text-slate-800 mb-4">Error Analysis</h3>
        <p className="text-slate-600">
          The synthetic model currently struggles with severe OCR degradation on address fields and 
          cross-script phonetic matching where the transliteration distance is large.
        </p>
        {/* Placeholder for confusion matrix or more metrics */}
      </div>
    </div>
  );
}
