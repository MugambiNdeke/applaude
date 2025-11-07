import React, { useState, useEffect } from 'react';
import Button from '../components/ui/Button';
import { Github, Zap, RefreshCw, Check, Clock, AlertTriangle, Download, GitPullRequest, Settings } from 'lucide-react';

const MOCK_PROJECTS = [
    { id: 1, name: 'my-ecomm-project', github_url: 'github.com/user/ecomm', runs_count: 5, last_run: '2025-11-05', is_connected: true },
    { id: 2, name: 'blog-cms-api', github_url: 'github.com/user/blog-api', runs_count: 12, last_run: '2025-10-29', is_connected: true },
    { id: 3, name: 'old-service-micro', github_url: 'github.com/user/service', runs_count: 0, last_run: null, is_connected: false },
];

const MOCK_RUNS = [
    { id: '1a2b3c', project_id: 1, status: 'COMPLETE', pr_url: 'github.com/pr/1', report_url: '/report/1', started_at: '11/07/2025 10:30', bugs_fixed: 3, run_type: 'FULL_STACK' },
    { id: '4d5e6f', project_id: 2, status: 'DEBUGGING', pr_url: null, report_url: null, started_at: '11/07/2025 11:15', bugs_fixed: 0, run_type: 'FULL_STACK' },
    { id: '7g8h9i', project_id: 1, status: 'FAILED', pr_url: null, report_url: null, started_at: '11/06/2025 14:00', bugs_fixed: 0, run_type: 'FRONTEND_ONLY' },
    { id: 'j0k1l2', project_id: 2, status: 'QUEUED', pr_url: null, report_url: null, started_at: '11/07/2025 11:30', bugs_fixed: 0, run_type: 'FULL_STACK' },
];

// MOCK DATA for the User's status
const MOCK_USER_STATUS = {
    runs_remaining: 47, // Linked to subscription data 
    plan: 'Monthly Startup',
    github_username: 'dev-architect-42',
};

const Dashboard = () => {
    const [userStatus, setUserStatus] = useState(MOCK_USER_STATUS);
    const [projects, setProjects] = useState(MOCK_PROJECTS);
    const [runs, setRuns] = useState(MOCK_RUNS);
    const [isRunModalOpen, setIsRunModalOpen] = useState(false);
    const [selectedProject, setSelectedProject] = useState(null);
    const [runType, setRunType] = useState('FULL_STACK');

    // Polling simulation for running tasks
    useEffect(() => {
        const interval = setInterval(() => {
            setRuns(prevRuns => prevRuns.map(run => {
                if (run.status === 'DEBUGGING') {
                    // Simulate status progress
                    const statuses = ['DEBUGGING', 'REPORTING', 'COMPLETE'];
                    const nextStatus = statuses[(statuses.indexOf(run.status) + 1) % statuses.length];
                    if (nextStatus === 'COMPLETE') {
                         return { ...run, status: nextStatus, pr_url: 'github.com/pr/new', bugs_fixed: 2 };
                    }
                    return { ...run, status: nextStatus };
                }
                return run;
            }));
        }, 5000); // Poll every 5 seconds
        
        return () => clearInterval(interval);
    }, []);


    const handleStartRunClick = (project) => {
        setSelectedProject(project);
        setIsRunModalOpen(true);
    };

    const handleConfirmRun = async () => {
        if (!selectedProject || userStatus.runs_remaining <= 0) return;

        // 1. Send POST request to /api/v1/projects/{id}/run/ [cite: 112]
        // This is where the core DRF view (start_run) is hit.
        
        // Mocking the API call
        const newRunId = `run-${Math.random().toString(36).substring(2, 8)}`;
        const newRun = { 
            id: newRunId, 
            project_id: selectedProject.id, 
            status: 'QUEUED', // 
            pr_url: null, 
            report_url: null, 
            started_at: new Date().toLocaleTimeString(),
            bugs_fixed: 0,
            run_type: runType,
        };

        setRuns(prevRuns => [newRun, ...prevRuns]);
        setUserStatus(prev => ({ ...prev, runs_remaining: prev.runs_remaining - 1 })); // Decrement run [cite: 115]
        setIsRunModalOpen(false);
        alert(`Autonomous Run for ${selectedProject.name} QUEUED!`);
    };
    
    // UI Utility: Maps status to color/icon
    const getStatusUI = (status) => {
        switch (status) {
            case 'COMPLETE': return { text: 'Complete', color: 'text-green-400', icon: Check };
            case 'DEBUGGING': 
            case 'REPORTING':
            case 'CLONING': return { text: status.charAt(0) + status.slice(1).toLowerCase(), color: 'text-electric-gold animate-pulse', icon: RefreshCw };
            case 'QUEUED': return { text: 'Queued', color: 'text-soft-white/50', icon: Clock };
            case 'FAILED': return { text: 'Failed', color: 'text-red-500', icon: AlertTriangle };
            default: return { text: status, color: 'text-soft-white', icon: Clock };
        }
    };
    
    // Reusable component for project row
    const ProjectRow = ({ project }) => (
        <div className="grid grid-cols-6 gap-4 items-center py-4 border-b border-soft-white/10 hover:bg-soft-white/5 transition-colors">
            <div className="col-span-2 flex items-center space-x-3">
                <Github className="w-5 h-5 text-soft-white/50" strokeWidth={1.5} />
                <span className="font-semibold text-soft-white">{project.name}</span>
            </div>
            <div className="col-span-2 text-sm text-soft-white/70 truncate">{project.github_url}</div>
            <div className="text-sm text-soft-white/70">{project.runs_count} Runs</div>
            <div className="flex justify-end space-x-2">
                <Button 
                    variant="primary" 
                    className="py-1 px-3 text-xs"
                    onClick={() => handleStartRunClick(project)}
                >
                    <Zap className="w-4 h-4 mr-2" strokeWidth={1.5} /> Start Autonomous Run
                </Button>
            </div>
        </div>
    );
    
    // Reusable component for run result row
    const RunRow = ({ run }) => {
        const ui = getStatusUI(run.status);
        const Icon = ui.icon;
        
        return (
            <div className="grid grid-cols-6 gap-4 items-center py-3 border-b border-soft-white/10 text-sm text-soft-white/70">
                <div className="col-span-2 flex items-center space-x-3">
                    <Icon className={`w-4 h-4 ${ui.color}`} strokeWidth={1.5} />
                    <span className={`font-medium ${ui.color}`}>{ui.text}</span>
                </div>
                <div className="text-soft-white">{MOCK_PROJECTS.find(p => p.id === run.project_id)?.name}</div>
                <div className="text-soft-white/50">{run.bugs_fixed > 0 ? `${run.bugs_fixed} Fixes` : 'No Fixes'}</div>
                <div className="text-soft-white/50">{run.started_at}</div>
                <div className="flex justify-end space-x-3">
                    {run.pr_url && (
                        <a href={run.pr_url} target="_blank" rel="noopener noreferrer">
                            <Button variant="secondary" className="py-1 px-3 text-xs">
                                <GitPullRequest className="w-4 h-4 mr-1" strokeWidth={1.5} /> PR
                            </Button>
                        </a>
                    )}
                    {run.report_url && (
                         <a href={run.report_url} target="_blank" rel="noopener noreferrer">
                            <Button variant="secondary" className="py-1 px-3 text-xs">
                                <Download className="w-4 h-4 mr-1" strokeWidth={1.5} /> Report
                            </Button>
                        </a>
                    )}
                </div>
            </div>
        );
    };


    // The main dashboard UI structure
    return (
        <div className="min-h-screen bg-luxury-black font-poppins text-soft-white p-4">
            <header className="max-w-7xl mx-auto py-6 flex justify-between items-center border-b border-soft-white/10 mb-8">
                <h1 className="text-3xl font-bold text-electric-gold tracking-wider">APPLAUDE / <span className="text-soft-white/80">Dashboard</span></h1>
                <div className="flex items-center space-x-4">
                    <span className="text-sm text-soft-white/70">Welcome, {MOCK_USER_STATUS.github_username}</span>
                    <Button variant="secondary" className="py-1 px-3 text-sm">
                        <Settings className="w-4 h-4 mr-2" strokeWidth={1.5} /> Account
                    </Button>
                </div>
            </header>

            <main className="max-w-7xl mx-auto space-y-12">
                
                {/* 1. Status and Runs Remaining Card */}
                <div className="bg-soft-white/5 p-6 rounded-xl border-t-4 border-electric-gold/50 shadow-lg">
                    <div className="flex justify-between items-center">
                        <h2 className="text-2xl font-bold text-soft-white">Subscription Status</h2>
                        <Button variant="primary" className="py-2 px-4 text-sm">Upgrade Plan</Button>
                    </div>
                    <div className="mt-4 flex space-x-8">
                        <div className="text-center p-4 bg-luxury-black rounded-lg border border-soft-white/10 flex-1">
                            <p className="text-4xl font-extrabold text-electric-gold">{userStatus.runs_remaining}</p>
                            <p className="text-sm text-soft-white/70 mt-1">Runs Remaining</p>
                        </div>
                        <div className="text-center p-4 bg-luxury-black rounded-lg border border-soft-white/10 flex-1">
                            <p className="text-xl font-bold text-soft-white">{userStatus.plan}</p>
                            <p className="text-sm text-soft-white/70 mt-1">Current Plan</p>
                        </div>
                    </div>
                </div>

                {/* 2. Connected Projects */}
                <section>
                    <h2 className="text-2xl font-bold text-soft-white mb-6">Connected Repositories ({projects.length})</h2>
                    <div className="bg-soft-white/5 p-6 rounded-xl border border-soft-white/10">
                        <div className="grid grid-cols-6 gap-4 items-center font-medium text-soft-white/70 border-b pb-2 mb-2">
                            <span className="col-span-2">Project</span>
                            <span className="col-span-2">GitHub URL</span>
                            <span>Total Runs</span>
                            <span className="text-right">Action</span>
                        </div>
                        {projects.filter(p => p.is_connected).map(p => <ProjectRow key={p.id} project={p} />)}
                        <div className="pt-4 flex justify-center">
                            <Button variant="secondary" className="text-sm">
                                <Github className="w-4 h-4 mr-2" strokeWidth={1.5} /> Connect New Repository
                            </Button>
                        </div>
                    </div>
                </section>
                
                {/* 3. Run History */}
                <section>
                    <h2 className="text-2xl font-bold text-soft-white mb-6">Autonomous Run History</h2>
                    <div className="bg-soft-white/5 p-6 rounded-xl border border-soft-white/10">
                         <div className="grid grid-cols-6 gap-4 items-center font-medium text-soft-white/70 border-b pb-2 mb-2 text-sm">
                            <span className="col-span-2">Status</span>
                            <span>Project</span>
                            <span>Fixes</span>
                            <span>Started At</span>
                            <span className="text-right">Artifacts</span>
                        </div>
                        {runs.map(run => <RunRow key={run.id} run={run} />)}
                    </div>
                </section>
            </main>
            
            {/* Run Confirmation Modal */}
            {isRunModalOpen && (
                <div className="fixed inset-0 bg-luxury-black/90 flex items-center justify-center z-50">
                    <div className="bg-soft-white/5 p-8 rounded-xl max-w-lg w-full border border-electric-gold/50 shadow-gold-glow">
                        <h3 className="text-xl font-bold text-soft-white mb-4">Start Autonomous Run</h3>
                        <p className="text-soft-white/70 mb-6">You are about to launch a Level 5 Autonomous Run on **{selectedProject.name}**. This will use **1** of your remaining **{userStatus.runs_remaining}** runs.</p>
                        
                        <div className="mb-6">
                            <label className="block text-sm font-medium text-soft-white/80 mb-2">Select Run Type:</label>
                            <div className="flex space-x-4">
                                <label className="flex items-center space-x-2 text-soft-white">
                                    <input 
                                        type="radio" 
                                        name="runType" 
                                        value="FULL_STACK" 
                                        checked={runType === 'FULL_STACK'} 
                                        onChange={() => setRunType('FULL_STACK')}
                                        className="text-electric-gold focus:ring-electric-gold bg-luxury-black border-soft-white/30"
                                    />
                                    <span>Test Full Stack (Frontend & Backend) [cite: 110]</span>
                                </label>
                                <label className="flex items-center space-x-2 text-soft-white">
                                    <input 
                                        type="radio" 
                                        name="runType" 
                                        value="FRONTEND_ONLY" 
                                        checked={runType === 'FRONTEND_ONLY'} 
                                        onChange={() => setRunType('FRONTEND_ONLY')}
                                        className="text-electric-gold focus:ring-electric-gold bg-luxury-black border-soft-white/30"
                                    />
                                    <span>Test Frontend UI Only [cite: 111]</span>
                                </label>
                            </div>
                        </div>

                        <div className="flex justify-end space-x-4">
                            <Button variant="secondary" onClick={() => setIsRunModalOpen(false)}>Cancel</Button>
                            <Button variant="primary" onClick={handleConfirmRun}>
                                <Zap className="w-4 h-4 mr-2" strokeWidth={1.5} /> Confirm & Launch
                            </Button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default Dashboard;
