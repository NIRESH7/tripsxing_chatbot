import React, { useState, useRef, useEffect } from 'react';
import { Send, User, Loader2, ArrowUp } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { sendMessage } from '../services/api';
import clsx from 'clsx';

const ChatInterface = () => {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [showScrollButton, setShowScrollButton] = useState(false);
    const messagesEndRef = useRef(null);
    const textareaRef = useRef(null);
    const scrollContainerRef = useRef(null);

    const handleScroll = () => {
        if (scrollContainerRef.current && scrollContainerRef.current.scrollTop > 300) {
            setShowScrollButton(true);
        } else {
            setShowScrollButton(false);
        }
    };

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "auto" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    useEffect(() => {
        if (textareaRef.current) {
            textareaRef.current.style.height = 'auto';
            textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 200)}px`;
        }
    }, [input]);

    const handleSend = async (e) => {
        if (e) e.preventDefault();
        if (!input.trim() || isLoading) return;

        const userMsg = { role: 'user', content: input, timestamp: new Date().toISOString() };
        setMessages(prev => [...prev, userMsg]);
        setInput('');
        if (textareaRef.current) textareaRef.current.style.height = 'auto';
        setIsLoading(true);

        try {
            const context = messages.slice(-5).map(m => ({ role: m.role === 'system' ? 'assistant' : m.role, content: m.content }));
            const response = await sendMessage(userMsg.content, context);
            const botMsg = {
                role: 'assistant',
                content: response.response,
                source: response.source,
                timestamp: new Date().toISOString()
            };
            setMessages(prev => [...prev, botMsg]);
        } catch (error) {
            setMessages(prev => [...prev, { role: 'assistant', content: "Sorry, I encountered an error. Please try again.", isError: true }]);
        } finally {
            setIsLoading(false);
        }
    };

    const handleKeyDown = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSend();
        }
    };

    return (
        <div className="flex-1 flex flex-col h-full relative w-full max-w-full">

            {/* Messages Area */}
            <div
                ref={scrollContainerRef}
                onScroll={handleScroll}
                className="flex-1 overflow-y-auto scroll-smooth w-full"
            >
                {messages.length === 0 ? (
                    <div className="h-full flex flex-col items-center justify-center p-8 text-center space-y-6">
                        <div className="bg-white p-4 rounded-full shadow-lg mb-4">
                            <img src="/logo.png" alt="Logo" className="w-16 h-16 object-contain" />
                        </div>
                        <h2 className="text-2xl font-semibold text-slate-800">How can I help you today?</h2>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 max-w-2xl w-full">
                            {['Plan a trip to Goa', 'Best hotels in Mumbai', 'Weekend getaways from Delhi', 'Houseboats in Kerala'].map((suggestion, i) => (
                                <button
                                    key={i}
                                    onClick={() => setInput(suggestion)}
                                    className="p-4 border border-slate-200 rounded-xl text-left hover:bg-slate-50 transition-colors text-slate-600 text-sm"
                                >
                                    {suggestion}
                                </button>
                            ))}
                        </div>
                    </div>
                ) : (
                    <div className="flex flex-col pb-32 pt-4 md:pt-10">
                        {messages.map((msg, index) => (
                            <div
                                key={index}
                                className={clsx(
                                    "w-full py-6 px-2 md:px-4 border-b-0",
                                    msg.role === 'user' ? "bg-white" : "bg-slate-50/50"
                                )}
                            >
                                <div className={clsx(
                                    "max-w-3xl mx-auto flex gap-4 md:gap-6",
                                    msg.role === 'user' ? "flex-row-reverse" : "flex-row" // ALIGNMENT LOGIC
                                )}>
                                    {/* Avatar */}
                                    <div className="flex-shrink-0 flex flex-col relative items-end">
                                        <div className="w-8 h-8 flex items-center justify-center">
                                            {msg.role === 'user' ? (
                                                <div className="w-8 h-8 bg-brand-blue rounded-md flex items-center justify-center text-white">
                                                    <User className="w-5 h-5" />
                                                </div>
                                            ) : (
                                                <div className="w-8 h-8 rounded-md overflow-hidden bg-white border border-slate-100 p-0.5">
                                                    <img src="/logo.png" alt="Bot" className="w-full h-full object-contain" />
                                                </div>
                                            )}
                                        </div>
                                    </div>

                                    {/* Message Content */}
                                    <div className={clsx(
                                        "relative flex-1 overflow-hidden flex flex-col",
                                        msg.role === 'user' ? "items-end" : "items-start"
                                    )}>
                                        <div className={clsx(
                                            "prose prose-slate leading-7 text-[15px] md:text-base inline-block text-left p-3 rounded-2xl max-w-[90%] md:max-w-[80%] shadow-sm break-words overflow-hidden line-clamp-6",
                                            // USER BUBBLE STYLE
                                            msg.role === 'user'
                                                ? "bg-brand-blue text-white rounded-tr-sm"
                                                : "text-slate-800"
                                        )}>
                                            <div className="prose prose-sm max-w-none prose-p:mb-1 prose-p:last:mb-0 prose-headings:font-bold prose-headings:text-sm prose-headings:mb-2 prose-ul:list-disc prose-ul:pl-4 prose-ul:mb-1 prose-li:mb-0.5">
                                                <ReactMarkdown
                                                    remarkPlugins={[remarkGfm]}
                                                    components={{
                                                        // Custom components to ensure specific styling matches the "clean" request
                                                        p: ({ node, ...props }) => <p className="mb-1 last:mb-0 leading-relaxed" {...props} />,
                                                        ul: ({ node, ...props }) => <ul className="list-disc pl-5 mb-1 text-slate-600 space-y-0" {...props} />,
                                                        ol: ({ node, ...props }) => <ol className="list-decimal pl-5 mb-1 text-slate-600 space-y-0" {...props} />,
                                                        li: ({ node, ...props }) => <li className="pl-1" {...props} />,
                                                        h1: ({ node, ...props }) => <h1 className="text-lg font-bold mt-3 mb-1 text-slate-900" {...props} />,
                                                        h2: ({ node, ...props }) => <h2 className="text-base font-bold mt-2 mb-1 text-slate-900" {...props} />,
                                                        h3: ({ node, ...props }) => <h3 className="text-sm font-bold mt-2 mb-1 text-slate-800 uppercase tracking-wide" {...props} />,
                                                        strong: ({ node, ...props }) => <span className="font-semibold text-slate-900" {...props} />,
                                                    }}
                                                >
                                                    {msg.content}
                                                </ReactMarkdown>
                                            </div>
                                            {/* Source Indicator */}
                                            {msg.source === 'database' && (
                                                <div className="mt-2 pt-2 border-t border-slate-100 flex items-center text-xs text-brand-blue font-medium">
                                                    <div className="w-1.5 h-1.5 rounded-full bg-brand-blue mr-1.5 animate-pulse"></div>
                                                    Verified Answer from Database
                                                </div>
                                            )}
                                        </div>
                                    </div>
                                </div>
                            </div>
                        ))}

                        {/* Loading State */}
                        {isLoading && (
                            <div className="w-full py-6 px-4 md:px-8 bg-slate-50/50">
                                <div className="max-w-3xl mx-auto flex gap-4 md:gap-6">
                                    <div className="w-8 h-8 rounded-md overflow-hidden bg-white border border-slate-100 p-0.5 flex-shrink-0">
                                        <img src="/logo.png" alt="Bot" className="w-full h-full object-contain animate-pulse" />
                                    </div>
                                    <div className="flex items-center">
                                        <span className="w-2 h-2 bg-slate-400 rounded-full animate-bounce mr-1"></span>
                                        <span className="w-2 h-2 bg-slate-400 rounded-full animate-bounce mr-1 delay-75"></span>
                                        <span className="w-2 h-2 bg-slate-400 rounded-full animate-bounce delay-150"></span>
                                    </div>
                                </div>
                            </div>
                        )}
                        <div ref={messagesEndRef} />
                    </div>
                )}
            </div>

            {/* Scroll to Top Button */}
            {
                showScrollButton && (
                    <button
                        onClick={() => scrollContainerRef.current?.scrollTo({ top: 0, behavior: 'smooth' })}
                        className="absolute bottom-36 right-4 p-3 bg-white border border-slate-200 shadow-xl rounded-full text-slate-500 hover:text-brand-blue hover:border-brand-blue transition-all z-20"
                    >
                        <ArrowUp className="w-5 h-5" />
                    </button>
                )
            }

            {/* Input Area - NO BORDERS */}
            <div className="absolute bottom-0 left-0 w-full bg-gradient-to-t from-white via-white to-transparent pt-10 pb-4 px-4">
                <div className="max-w-3xl mx-auto">
                    {/* Removed 'border', 'ring', 'focus-within' classes to eliminate borders */}
                    <div className="relative flex items-end w-full p-3 bg-white rounded-2xl shadow-[0_0_15px_rgba(0,0,0,0.1)] transition-all">
                        <textarea
                            ref={textareaRef}
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            onKeyDown={handleKeyDown}
                            placeholder="Message TripsXing..."
                            // Added outline-none focus:outline-none focus:ring-0
                            className="w-full max-h-[200px] bg-transparent border-0 outline-none focus:outline-none focus:ring-0 p-0 pr-10 resize-none text-slate-800 placeholder-slate-400 leading-6"
                            rows={1}
                        />
                        <button
                            onClick={handleSend}
                            disabled={!input.trim() || isLoading}
                            className={clsx(
                                "absolute bottom-2.5 right-2.5 p-1.5 rounded-lg transition-colors",
                                input.trim() && !isLoading
                                    ? "bg-brand-blue text-white hover:bg-blue-600"
                                    : "bg-slate-100 text-slate-400 cursor-not-allowed"
                            )}
                        >
                            <Send className="w-4 h-4" />
                        </button>
                    </div>

                </div>
            </div>
        </div >
    );
};

export default ChatInterface;
