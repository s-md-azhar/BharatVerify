export function AuditTrail() {
  const events = [
    { time: '10:42:01 AM', event: 'CASE_CREATED', status: 'SUCCESS' },
    { time: '10:42:05 AM', event: 'DOCUMENT_UPLOADED', status: 'SUCCESS' },
    { time: '10:42:08 AM', event: 'OCR_STARTED', status: 'SUCCESS' },
    { time: '10:42:15 AM', event: 'OCR_COMPLETED', status: 'SUCCESS' },
    { time: '10:42:16 AM', event: 'FIELDS_EXTRACTED', status: 'SUCCESS' },
    { time: '10:42:18 AM', event: 'MATCHING_STARTED', status: 'SUCCESS' },
    { time: '10:42:20 AM', event: 'DECISION_CREATED', status: 'SUCCESS' },
  ];

  return (
    <div className="card p-8">
      <h2 className="text-lg font-semibold text-slate-900 mb-6">System Audit Trail</h2>
      <div className="flow-root">
        <ul className="-mb-8">
          {events.map((event, idx) => (
            <li key={idx}>
              <div className="relative pb-8">
                {idx !== events.length - 1 ? (
                  <span className="absolute top-4 left-4 -ml-px h-full w-0.5 bg-slate-200" aria-hidden="true"></span>
                ) : null}
                <div className="relative flex space-x-3">
                  <div>
                    <span className="h-8 w-8 rounded-full bg-slate-100 flex items-center justify-center ring-8 ring-white">
                      <div className="h-2.5 w-2.5 rounded-full bg-primary-600"></div>
                    </span>
                  </div>
                  <div className="min-w-0 flex-1 pt-1 flex justify-between space-x-4">
                    <div>
                      <p className="text-sm text-slate-500 font-mono">{event.event}</p>
                    </div>
                    <div className="text-right text-sm whitespace-nowrap text-slate-500">
                      <time>{event.time}</time>
                      <span className="ml-3 inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-emerald-100 text-emerald-800">
                        {event.status}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
