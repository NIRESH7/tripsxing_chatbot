import React, { useState } from 'react';
import ChatInterface from './components/ChatInterface';
import { Menu, Plus, MessageSquare, Settings, LogOut } from 'lucide-react';

function App() {
    const [isSidebarOpen, setIsSidebarOpen] = useState(false);

    return (
        <div className="flex h-screen bg-white font-sans overflow-hidden">
            {/* Mobile Sidebar Overlay */}
            {isSidebarOpen && (
                <div
                    className="fixed inset-0 bg-black/50 z-20 md:hidden"
                    onClick={() => setIsSidebarOpen(false)}
                ></div>
            )}

            {/* Sidebar (ChatGPT style) */}
            <aside className={`
                fixed inset-y-0 left-0 z-30
                w-[260px] bg-slate-900 text-slate-100 flex flex-col transition-transform duration-300 ease-in-out
                ${isSidebarOpen ? 'translate-x-0' : '-translate-x-full'}
                md:translate-x-0 md:static
            `}>
                <div className="p-3 flex-none">
                    <button className="flex items-center gap-3 w-full px-3 py-3 rounded-md border border-slate-700 hover:bg-slate-800 transition-colors text-sm text-left">
                        <Plus className="w-4 h-4" />
                        <span>New chat</span>
                    </button>
                </div>

                <div className="flex-1 overflow-y-auto px-3 py-2">
                    <div className="text-xs font-medium text-slate-500 mb-2 px-3">Today</div>
                    <button className="flex items-center gap-3 w-full px-3 py-3 rounded-md hover:bg-slate-800 transition-colors text-sm text-left truncate group">
                        <MessageSquare className="w-4 h-4 text-slate-500 group-hover:text-slate-300" />
                        <span className="truncate">Trip to Paris</span>
                    </button>
                    <button className="flex items-center gap-3 w-full px-3 py-3 rounded-md hover:bg-slate-800 transition-colors text-sm text-left truncate group">
                        <MessageSquare className="w-4 h-4 text-slate-500 group-hover:text-slate-300" />
                        <span className="truncate">Travel Itinerary</span>
                    </button>
                </div>

                <div className="p-3 border-t border-slate-700 flex-none">
                    <button className="flex items-center gap-3 w-full px-3 py-3 rounded-md hover:bg-slate-800 transition-colors text-sm text-left">
                        <div className="w-8 h-8 rounded-full bg-brand-red flex items-center justify-center text-white font-bold">
                            U
                        </div>
                        <div className="flex-1">
                            <div className="font-medium">User Account</div>
                            <div className="text-xs text-slate-400">Pro Plan</div>
                        </div>
                    </button>
                </div>
            </aside>

            {/* Main Content Area */}
            <main className="flex-1 flex flex-col h-full relative bg-white pt-14 md:pt-0">
                {/* Mobile Header - FIXED */}
                <header className="fixed top-0 left-0 right-0 z-20 bg-white/95 backdrop-blur-sm flex items-center p-2 md:hidden border-b border-slate-100 h-14 shadow-sm">
                    <button
                        onClick={() => setIsSidebarOpen(true)}
                        className="p-2 hover:bg-slate-100 rounded-md"
                    >
                        <Menu className="w-6 h-6 text-slate-600" />
                    </button>
                    <img src="/logo.png" alt="TripsXing" className="h-8 w-auto mx-auto" />
                    <div className="w-10"></div> {/* Spacer for center alignment */}
                </header>

                {/* Desktop Model Selector / Header */}
                <header className="hidden md:flex items-center p-3 absolute top-0 left-0 w-full z-10">
                    <div className="px-4 py-2 rounded-xl bg-slate-100 text-slate-600 font-medium text-sm flex items-center gap-2 cursor-pointer hover:bg-slate-200 transition-colors mx-auto">
                        <span>TripsXing 4.0</span>
                        <span className="w-2 h-2 rounded-full bg-brand-blue"></span>
                    </div>
                </header>

                {/* Chat Interface takes up remaining space */}
                <ChatInterface />
            </main>
        </div>
    );
}

export default App;
