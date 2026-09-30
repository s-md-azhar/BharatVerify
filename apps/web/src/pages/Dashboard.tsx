import { BarChart, Users, AlertCircle, CheckCircle } from 'lucide-react';

export function Dashboard() {
  const stats = [
    { name: 'Total Cases', value: '1,248', icon: Users, color: 'text-blue-600', bg: 'bg-blue-100' },
    { name: 'Verified', value: '1,024', icon: CheckCircle, color: 'text-emerald-600', bg: 'bg-emerald-100' },
    { name: 'Pending Review', value: '143', icon: AlertCircle, color: 'text-amber-600', bg: 'bg-amber-100' },
    { name: 'Mismatch / Rejected', value: '81', icon: BarChart, color: 'text-rose-600', bg: 'bg-rose-100' },
  ];

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat) => (
          <div key={stat.name} className="card p-6 flex items-center">
            <div className={`p-3 rounded-lg ${stat.bg} ${stat.color} mr-4`}>
              <stat.icon className="w-6 h-6" />
            </div>
            <div>
              <p className="text-sm font-medium text-slate-500">{stat.name}</p>
              <p className="text-2xl font-semibold text-slate-900">{stat.value}</p>
            </div>
          </div>
        ))}
      </div>
      
      <div className="card p-6 h-64 flex items-center justify-center text-slate-400">
        Chart placeholder (e.g. Verification success rate over time)
      </div>
    </div>
  );
}
