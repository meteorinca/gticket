import re
import os

filepath = 'index.html'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Fix "Perseverence" -> "Perseverance" (except in image filenames)
# We will just replace perseverence with perseverance in CSS classes, IDs, and text
content = content.replace('.coin-perseverence', '.coin-perseverance')
content = content.replace('data-coin="perseverence"', 'data-coin="perseverance"')
content = content.replace('id="curve-perseverence"', 'id="curve-perseverance"')
content = content.replace('href="#curve-perseverence"', 'href="#curve-perseverance"')
content = content.replace('>PERSEVERENCE<', '>PERSEVERANCE<')
content = content.replace('id="namePerseverence"', 'id="namePerseverance"')
content = content.replace('namePerseverence =', 'namePerseverance =')
content = content.replace('namePerseverence.', 'namePerseverance.')
content = content.replace('perseverence:', 'perseverance:')

# 2. Add AudioContext for subtle sounds
audio_script = """
            // ─────────────────────────────────────
            // AUDIO DESIGN (Web Audio API)
            // ─────────────────────────────────────
            const AudioContext = window.AudioContext || window.webkitAudioContext;
            let audioCtx = null;
            let humOsc = null;
            let humGain = null;

            function initAudio() {
                if (!audioCtx) {
                    audioCtx = new AudioContext();
                    
                    // Ambient hum
                    humOsc = audioCtx.createOscillator();
                    humOsc.type = 'sine';
                    humOsc.frequency.value = 55; // Deep hum
                    
                    humGain = audioCtx.createGain();
                    humGain.gain.value = 0.05; // Very subtle
                    
                    humOsc.connect(humGain);
                    humGain.connect(audioCtx.destination);
                    humOsc.start();
                }
                if (audioCtx.state === 'suspended') {
                    audioCtx.resume();
                }
            }

            function playChime() {
                if (!audioCtx) return;
                const osc = audioCtx.createOscillator();
                const gain = audioCtx.createGain();
                osc.type = 'sine';
                osc.frequency.setValueAtTime(880, audioCtx.currentTime); // A5
                osc.frequency.exponentialRampToValueAtTime(1760, audioCtx.currentTime + 0.1); // Slide up
                
                gain.gain.setValueAtTime(0, audioCtx.currentTime);
                gain.gain.linearRampToValueAtTime(0.1, audioCtx.currentTime + 0.02);
                gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 1.5);
                
                osc.connect(gain);
                gain.connect(audioCtx.destination);
                osc.start();
                osc.stop(audioCtx.currentTime + 1.5);
            }

            function playClink() {
                if (!audioCtx) return;
                const osc = audioCtx.createOscillator();
                const gain = audioCtx.createGain();
                osc.type = 'triangle';
                osc.frequency.setValueAtTime(1200, audioCtx.currentTime);
                osc.frequency.exponentialRampToValueAtTime(800, audioCtx.currentTime + 0.1);
                
                gain.gain.setValueAtTime(0.1, audioCtx.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.3);
                
                osc.connect(gain);
                gain.connect(audioCtx.destination);
                osc.start();
                osc.stop(audioCtx.currentTime + 0.3);
            }

            // Initialize audio on first user interaction
            document.body.addEventListener('click', initAudio, { once: true });
"""
# Insert audio script before Initialization Log
content = content.replace('// ─────────────────────────────────────\n            // INITIALIZATION LOG', audio_script + '\n            // ─────────────────────────────────────\n            // INITIALIZATION LOG')

# Trigger playChime and playClink
content = content.replace('openModal();', 'playChime();\n                openModal();')
content = content.replace('ticketTitle.innerHTML = `Golden Ticket', 'playChime();\n                    ticketTitle.innerHTML = `Golden Ticket')

# In coin click listener, add playClink() and ticket opacity logic
coin_click_logic_old = """
                    const coinId = this.getAttribute('data-coin');
                    if (robotData[coinId]) {
                        // Reset animations
                        robotOverlay.classList.remove('active');
"""
coin_click_logic_new = """
                    const coinId = this.getAttribute('data-coin');
                    if (robotData[coinId]) {
                        playClink();
                        
                        // Hide golden ticket to see full image
                        ticket.style.opacity = '0';
                        ticket.style.transition = 'opacity 0.3s ease';

                        // Reset animations
                        robotOverlay.classList.remove('active');
"""
content = content.replace(coin_click_logic_old, coin_click_logic_new)

# 3. Enhance Robot Overlay & Dismissible
# Add dismiss logic to robot overlay
robot_dismiss = """
            robotOverlay.addEventListener('click', function() {
                robotOverlay.classList.remove('active');
                ticket.style.opacity = '1';
                clearTimeout(robotTimeout);
            });
"""
content = content.replace('const robotImage = document.getElementById(\'robotImage\');', 'const robotImage = document.getElementById(\'robotImage\');\n' + robot_dismiss)

# Restore ticket opacity when timeout finishes
timeout_old = """
                        robotTimeout = setTimeout(() => {
                            robotOverlay.classList.remove('active');
                        }, 7000);
"""
timeout_new = """
                        robotTimeout = setTimeout(() => {
                            robotOverlay.classList.remove('active');
                            ticket.style.opacity = '1';
                        }, 7000);
"""
content = content.replace(timeout_old, timeout_new)

# Add pointer-events to robotOverlay so it can be clicked, and add sci-fi transition CSS
css_old = """
        .robot-overlay {
            position: fixed;
            inset: 0;
            z-index: 0;
            background: transparent;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            opacity: 0;
            pointer-events: none;
            transition: opacity 2s ease;
        }

        .robot-overlay.active {
            opacity: 0.4;
        }

        .robot-image {
            max-width: 100vw;
            max-height: 100vh;
            object-fit: contain;
            transform: scale(0.85);
            transition: transform 7s ease-out;
            filter: drop-shadow(0 0 40px rgba(218, 165, 32, 0.4));
        }

        .robot-overlay.active .robot-image {
            transform: scale(1.05);
        }
"""
css_new = """
        .robot-overlay {
            position: fixed;
            inset: 0;
            z-index: 50; /* Bring above coins to allow clicking */
            background: transparent;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            opacity: 0;
            pointer-events: none;
            transition: opacity 1.5s ease;
            cursor: pointer;
        }

        .robot-overlay.active {
            opacity: 0.85; /* Make it more visible since ticket hides */
            pointer-events: auto; /* Allow clicking to dismiss */
            background: radial-gradient(circle at center, rgba(0,0,0,0.6) 0%, rgba(0,0,0,0.95) 100%);
        }

        .robot-image {
            max-width: 100vw;
            max-height: 100vh;
            object-fit: contain;
            transform: scale(0.85);
            transition: transform 7s ease-out, filter 2s ease;
            filter: drop-shadow(0 0 40px rgba(218, 165, 32, 0.4)) contrast(1.5) brightness(1.5) sepia(1) hue-rotate(180deg) blur(10px);
            opacity: 0;
        }

        .robot-overlay.active .robot-image {
            transform: scale(1.05);
            filter: drop-shadow(0 0 40px rgba(218, 165, 32, 0.4)) contrast(1) brightness(1) sepia(0) hue-rotate(0deg) blur(0px);
            opacity: 1;
            transition: transform 7s ease-out, filter 1.5s ease-out, opacity 1s ease-in;
        }
        
        .robot-overlay::before {
            content: '';
            position: absolute;
            inset: 0;
            background: repeating-linear-gradient(
                0deg,
                rgba(0, 0, 0, 0.1),
                rgba(0, 0, 0, 0.1) 1px,
                transparent 1px,
                transparent 2px
            );
            pointer-events: none;
            z-index: 10;
            opacity: 0;
            transition: opacity 1.5s ease;
        }
        
        .robot-overlay.active::before {
            opacity: 0.3;
        }
"""
content = content.replace(css_old, css_new)

# 4. Advanced Lighting & Tactility
# Coin hover scale
css_coin_old = """
        .coin:hover .coin-bg {
            filter: brightness(1.25);
        }
"""
css_coin_new = """
        .coin {
            transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }
        .coin:hover {
            transform: scale(1.1);
        }
        .coin:hover .coin-bg {
            filter: brightness(1.25);
        }
"""
# Note: .coin already has transition in my replacement, wait, let me just add .coin:hover { transform: scale(1.1); }
content = content.replace(css_coin_old, css_coin_old + "\n        .coin:hover {\n            transform: scale(1.1);\n            z-index: 20;\n        }\n")


# Embossed text on ticket title
css_title_old = """
            text-shadow:
                0 1px 0 rgba(255, 255, 255, 0.5),
                0 2px 4px rgba(0, 0, 0, 0.1);
"""
css_title_new = """
            text-shadow:
                0 -1px 1px rgba(0, 0, 0, 0.5),
                0 1px 1px rgba(255, 255, 255, 0.8),
                0 2px 4px rgba(0, 0, 0, 0.2),
                0 4px 8px rgba(0, 0, 0, 0.1);
"""
content = content.replace(css_title_old, css_title_new)

# Dynamic Shimmer
# In handleMouseMove:
dynamic_shimmer_js = """
                // Apply rotation
                rotator.style.transform = `rotateY(${rotateY.toFixed(2)}deg) rotateX(${rotateX.toFixed(2)}deg)`;
"""
dynamic_shimmer_new = """
                // Apply rotation
                rotator.style.transform = `rotateY(${rotateY.toFixed(2)}deg) rotateX(${rotateX.toFixed(2)}deg)`;
                
                // Dynamic shimmer position
                const shimmerEl = ticket.querySelector('.shimmer');
                if (shimmerEl) {
                    const shimmerX = (nx + 1) * 50; // 0 to 100
                    const shimmerY = (ny + 1) * 50;
                    shimmerEl.style.background = `linear-gradient(115deg, 
                        transparent 0%, 
                        transparent calc(${shimmerX}% - 15%), 
                        rgba(255, 255, 255, 0) calc(${shimmerX}% - 5%), 
                        rgba(255, 255, 255, 0.55) ${shimmerX}%, 
                        rgba(255, 255, 255, 0.7) calc(${shimmerX}% + 3%), 
                        rgba(255, 255, 255, 0.55) calc(${shimmerX}% + 6%), 
                        rgba(255, 255, 255, 0) calc(${shimmerX}% + 10%), 
                        transparent calc(${shimmerX}% + 15%), 
                        transparent 100%)`;
                    shimmerEl.style.animation = 'none'; // Disable auto-sweep while hovering
                }
"""
content = content.replace(dynamic_shimmer_js, dynamic_shimmer_new)

# Re-enable animation on mouse leave
leave_old = """
                rotator.style.transform = '';
                rotator.classList.add('swaying');
"""
leave_new = """
                rotator.style.transform = '';
                rotator.classList.add('swaying');
                const shimmerEl = ticket.querySelector('.shimmer');
                if (shimmerEl) {
                    shimmerEl.style.background = ''; // reset to CSS defined
                    shimmerEl.style.animation = 'shimmerSweep 4.5s ease-in-out infinite';
                }
"""
content = content.replace(leave_old, leave_new)
content = content.replace('isMouseOverScene = false;\n                    rotator.style.transform = \'\';\n                    rotator.classList.add(\'swaying\');', 'isMouseOverScene = false;\n                    rotator.style.transform = \'\';\n                    rotator.classList.add(\'swaying\');\n                    const sEl = ticket.querySelector(\'.shimmer\'); if (sEl) { sEl.style.background=\'\'; sEl.style.animation=\'shimmerSweep 4.5s ease-in-out infinite\'; }')

# 5. Name Input Polish
# Modify applyName to use placeholder if blank
apply_name_old = """
            function applyName(name) {
                const displayName = name.trim() || '\\u2726';
                userName = name.trim();
"""
apply_name_new = """
            function applyName(name) {
                const placeholders = ["Space Traveler", "Explorer", "Willy Wonka", "Star Gazer", "Astronaut"];
                let finalName = name.trim();
                if (!finalName) {
                    finalName = placeholders[Math.floor(Math.random() * placeholders.length)];
                }
                const displayName = finalName;
                userName = finalName;
"""
content = content.replace(apply_name_old, apply_name_new)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Done")
