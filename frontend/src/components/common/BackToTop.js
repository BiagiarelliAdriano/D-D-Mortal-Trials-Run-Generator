import React, { useState, useEffect, useCallback } from 'react';
import '../../styles/BackToTop.css';

/**
 * BackToTop Component
 * @param {string} containerSelector - Optional CSS selector for internal scroll containers.
 * @param {number} threshold - Scroll distance before button appears (default: 400).
 * @param {number} jumpThreshold - Scroll distance before switching to "instant cut" (default: 2500).
 */
const BackToTop = ({ containerSelector, threshold = 400, jumpThreshold = 2500 }) => {
    const [isVisible, setIsVisible] = useState(false);

    const handleScroll = useCallback(() => {
        const scrollPos = containerSelector 
            ? document.querySelector(containerSelector)?.scrollTop ?? 0
            : window.scrollY;

        setIsVisible(scrollPos > threshold);
    }, [containerSelector, threshold]);

    useEffect(() => {
        const target = containerSelector 
            ? document.querySelector(containerSelector) 
            : window;

        if (target) {
            target.addEventListener('scroll', handleScroll);
            // Initial check
            handleScroll();
            return () => target.removeEventListener('scroll', handleScroll);
        }
    }, [containerSelector, handleScroll]);

    const scrollToTop = () => {
        if (containerSelector) {
            const el = document.querySelector(containerSelector);
            if (el) {
                const behavior = el.scrollTop > jumpThreshold ? 'auto' : 'smooth';
                el.scrollTo({ top: 0, behavior });
            }
        } else {
            const behavior = window.scrollY > jumpThreshold ? 'auto' : 'smooth';
            window.scrollTo({ top: 0, behavior });
        }
    };

    return (
        <button 
            className={`back-to-top-btn ${isVisible ? 'visible' : ''}`}
            onClick={scrollToTop}
            aria-label="Back to Top"
        >
            <i className="fa-solid fa-chevron-up"></i>
        </button>
    );
};

export default BackToTop;
