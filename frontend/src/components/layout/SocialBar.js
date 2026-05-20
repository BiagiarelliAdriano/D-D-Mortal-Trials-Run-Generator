import React from 'react';
import '../../styles/SocialBar.css';

const SocialBar = () => {
    return (
        <div className="global-social-bar">
            <a 
                href="https://discord.gg/CmNqX7Mrtp" 
                target="_blank" 
                rel="noopener noreferrer" 
                className="social-icon discord"
                title="Join our Discord"
            >
                <i className="fa-brands fa-discord"></i>
            </a>
            <a 
                href="https://www.patreon.com/c/TheMortalTrials" 
                target="_blank" 
                rel="noopener noreferrer" 
                className="social-icon patreon"
                title="Support us on Patreon"
            >
                <i className="fa-brands fa-patreon"></i>
            </a>
            <button 
                onClick={() => window.open('/report', '_blank')}
                className="social-icon bug-report"
                title="Report Feedback or a Bug"
            >
                <i className="fa-solid fa-bug"></i>
            </button>

        </div>
    );
};

export default SocialBar;
