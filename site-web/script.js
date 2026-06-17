// ========================================
// 📝 DONNÉES MODULAIRES - MODIFIEZ ICI
// ========================================
// 
// INSTRUCTIONS :
// - Pour AJOUTER un projet : Ajoutez un objet dans MES_PROJETS
// - Pour SUPPRIMER : Supprimez l'objet correspondant
// - Pour AJOUTER une compétence : Ajoutez dans le tableau "items"
//
// ========================================

// ----------------------------------------
// 🚀 MES PROJETS
// ----------------------------------------

const MES_PROJETS = [
    {
        titre: "Agent RGPD — LÉA",
        description: "LÉA (Liberté, Expertise, Assistance) — IA conversationnelle entièrement locale dédiée à la conformité RGPD et à l'assistance juridique.",
        tags: ["Python", "IA Locale", "RGPD", "LLM"],
        lien: "https://github.com/Dow08/Agent_RGPD",
        icone: "🤖",
        date: "Fév 2026"
    },
    {
        titre: "Mon Portfolio",
        description: "Portfolio cybersécurité avec pipeline CyberPulse : scraping, traduction IA, génération audio et déploiement automatisé via GitHub Actions.",
        tags: ["HTML", "CSS", "JavaScript", "Python", "GitHub Actions"],
        lien: "https://github.com/Dow08/Mon_Portfolio",
        icone: "🌐",
        date: "Fév 2026"
    },
    {
        titre: "Moltbot v1",
        description: "Bot personnalisé Moltbot v1 — automatisation d'interactions et intégration de fonctionnalités intelligentes.",
        tags: ["TypeScript", "Bot", "Automatisation"],
        lien: "https://github.com/Dow08/Moltbot",
        icone: "⚡",
        date: "Fév 2026"
    },
    {
        titre: "ActuCybersécurité",
        description: "Scraper d'actualités cybersécurité avec génération automatique de podcasts audio — ancêtre du pipeline CyberPulse.",
        tags: ["Python", "Scraping", "Podcast", "Cybersécurité"],
        lien: "https://github.com/Dow08/ActuCybersecurite",
        icone: "📡",
        date: "Jan 2026"
    },
    {
        titre: "TRP",
        description: "Projet de développement web HTML — travaux pratiques et expérimentations front-end.",
        tags: ["HTML", "Web"],
        lien: "https://github.com/Dow08/TRP",
        icone: "📄",
        date: "Oct 2025"
    }
];

// ----------------------------------------
// 🎯 MES COMPÉTENCES
// ----------------------------------------

const MES_COMPETENCES = [
    {
        categorie: "🛡️ Cybersécurité & Sécurité Offensive",
        icone: "fas fa-shield-alt",
        couleur: "cyber",
        items: [
            { nom: "Test d'intrusion (Pentest)", niveau: 80, badge: "Jedha" },
            { nom: "Sécurité Web", niveau: 80, badge: "Jedha" },
            { nom: "Sécurité Réseau", niveau: 75, badge: "Jedha" },
            { nom: "Sécurité Système", niveau: 75, badge: "Jedha" },
            { nom: "Source Intelligence (OSINT)", niveau: 70, badge: "Jedha" },
            { nom: "Cybersécurité (générale)", niveau: 85, badge: null },
            { nom: "CTF & Challenges (TryHackMe)", niveau: 70, badge: null }
        ]
    },
    {
        categorie: "💻 Informatique & Développement",
        icone: "fas fa-code",
        couleur: "dev",
        items: [
            { nom: "Prompting IA & LLM", niveau: 85, badge: "Jedha" },
            { nom: "Administration Réseau", niveau: 75, badge: "Jedha" },
            { nom: "Python", niveau: 70, badge: null },
            { nom: "TypeScript / Bots", niveau: 60, badge: null },
            { nom: "HTML / CSS / JS", niveau: 65, badge: null },
            { nom: "Maintenance & Réparation Informatique", niveau: 90, badge: null },
            { nom: "Installation Matériel & Dépannage", niveau: 90, badge: null },
            { nom: "Conseil en Informatique", niveau: 85, badge: null },
            { nom: "GitHub Actions & CI/CD", niveau: 65, badge: null }
        ]
    },
    {
        categorie: "📊 Management & Commerce",
        icone: "fas fa-chart-bar",
        couleur: "management",
        items: [
            { nom: "Gestion de Magasin & Encadrement Équipe", niveau: 95, badge: "Carrefour" },
            { nom: "Recrutement & RH", niveau: 85, badge: "Carrefour" },
            { nom: "E-commerce & Optimisation", niveau: 80, badge: "Carrefour" },
            { nom: "Stratégie de Vente & Marketing", niveau: 85, badge: "Carrefour" },
            { nom: "Analyse Marketing & Merchandising", niveau: 80, badge: "Carrefour" },
            { nom: "Logistique & Analyse", niveau: 75, badge: "Carrefour" },
            { nom: "Comptabilité & Gestion", niveau: 70, badge: "Carrefour" },
            { nom: "Développement des Ventes", niveau: 85, badge: "Carrefour" }
        ]
    },
    {
        categorie: "🤝 Soft Skills & Transversal",
        icone: "fas fa-users",
        couleur: "soft",
        items: [
            { nom: "Adaptabilité", niveau: 95, badge: null },
            { nom: "Prise d'initiative", niveau: 90, badge: null },
            { nom: "Esprit d'équipe", niveau: 90, badge: null },
            { nom: "Sens de l'organisation", niveau: 90, badge: null },
            { nom: "Autonomie", niveau: 90, badge: null },
            { nom: "Communication", niveau: 85, badge: null },
            { nom: "Résolution de problèmes", niveau: 85, badge: null },
            { nom: "Relations publiques", niveau: 75, badge: null }
        ]
    }
];

// ----------------------------------------
// 📊 MES STATS
// ----------------------------------------

const HERO_BADGES = [
    { label: 'G.R.C Consulting', icone: '📋', color: 'gold' },
    { label: 'Cybersécurité', icone: '🛡️', color: 'cyber' },
    { label: 'Pentest Junior & OSINT', icone: '🔍', color: 'cyber' },
    { label: 'IA & Automatisation', icone: '🤖', color: 'purple' },
    { label: 'Administration Sys.', icone: '🖥️', color: 'green' }
];

// ----------------------------------------
// 📬 INFOS CONTACT
// ----------------------------------------

const INFOS_CONTACT = {
    email: "Dow@ikmail.com",
    localisation: "France",
    disponibilite: "Ouvert aux opportunités",
    intro: "Je suis toujours ouvert aux discussions sur la cybersécurité, les opportunités de stage/alternance, ou simplement pour échanger sur les dernières techniques de sécurité offensive et défensive.",

    reseaux: [
        { nom: "GitHub", icone: "fab fa-github", url: "https://github.com/Dow08" },
        { nom: "LinkedIn", icone: "fab fa-linkedin", url: "https://www.linkedin.com/in/dorian-poncelet-1807612b5" },
        { nom: "Twitter", icone: "fab fa-twitter", url: "https://twitter.com/Dow163877" }
    ],

    ctf: [
        { nom: "TryHackMe", icone: "fas fa-flag", url: "https://tryhackme.com/p/seallia81", texte: "Voir mon profil TryHackMe" },
        { nom: "HackTheBox", icone: "fas fa-cube", url: "https://ctf.hackthebox.com/user/profile/1010141", texte: "Voir mon profil HackTheBox" }
    ]
};

// ========================================
// 🌌 ENHANCED PARTICLE SYSTEM
// ========================================

class ParticleSystem {
    constructor(canvas) {
        this.canvas = canvas;
        this.ctx = canvas.getContext('2d');
        this.particles = [];
        this.mouse = { x: null, y: null };
        this.particleCount = 100;
        this.connectionDistance = 150;
        this.mouseRadius = 100;

        this.colors = ['#00ff46', '#8b5cf6', '#3b82f6', '#00d4ff'];

        this.resize();
        this.init();
        this.animate();

        window.addEventListener('resize', () => this.resize());
        window.addEventListener('mousemove', (e) => {
            this.mouse.x = e.clientX;
            this.mouse.y = e.clientY;
        });
    }

    resize() {
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
    }

    init() {
        this.particles = [];
        for (let i = 0; i < this.particleCount; i++) {
            const color = this.colors[Math.floor(Math.random() * this.colors.length)];
            this.particles.push({
                x: Math.random() * this.canvas.width,
                y: Math.random() * this.canvas.height,
                vx: (Math.random() - 0.5) * 0.5,
                vy: (Math.random() - 0.5) * 0.5,
                radius: Math.random() * 2 + 1,
                color: color,
                baseOpacity: Math.random() * 0.5 + 0.3,
                pulseSpeed: Math.random() * 0.02 + 0.01,
                pulseOffset: Math.random() * Math.PI * 2
            });
        }
    }

    animate() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

        const time = Date.now() * 0.001;

        this.particles.forEach((p, i) => {
            // Mouse interaction
            if (this.mouse.x && this.mouse.y) {
                const dx = this.mouse.x - p.x;
                const dy = this.mouse.y - p.y;
                const dist = Math.sqrt(dx * dx + dy * dy);

                if (dist < this.mouseRadius) {
                    const force = (this.mouseRadius - dist) / this.mouseRadius;
                    p.vx -= (dx / dist) * force * 0.5;
                    p.vy -= (dy / dist) * force * 0.5;
                }
            }

            // Move
            p.x += p.vx;
            p.y += p.vy;

            // Friction
            p.vx *= 0.99;
            p.vy *= 0.99;

            // Random movement
            p.vx += (Math.random() - 0.5) * 0.1;
            p.vy += (Math.random() - 0.5) * 0.1;

            // Bounce
            if (p.x < 0 || p.x > this.canvas.width) p.vx *= -1;
            if (p.y < 0 || p.y > this.canvas.height) p.vy *= -1;

            // Pulsing opacity
            const pulse = Math.sin(time * p.pulseSpeed * 10 + p.pulseOffset);
            const opacity = p.baseOpacity + pulse * 0.2;

            // Draw particle with glow
            this.ctx.beginPath();
            this.ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
            this.ctx.fillStyle = p.color.replace(')', `, ${opacity})`).replace('rgb', 'rgba').replace('#', '');

            // Convert hex to rgba for glow
            const hexToRgba = (hex, alpha) => {
                const r = parseInt(hex.slice(1, 3), 16);
                const g = parseInt(hex.slice(3, 5), 16);
                const b = parseInt(hex.slice(5, 7), 16);
                return `rgba(${r}, ${g}, ${b}, ${alpha})`;
            };

            this.ctx.fillStyle = hexToRgba(p.color, opacity);
            this.ctx.shadowBlur = 15;
            this.ctx.shadowColor = p.color;
            this.ctx.fill();
            this.ctx.shadowBlur = 0;

            // Connections
            for (let j = i + 1; j < this.particles.length; j++) {
                const p2 = this.particles[j];
                const dx = p.x - p2.x;
                const dy = p.y - p2.y;
                const distance = Math.sqrt(dx * dx + dy * dy);

                if (distance < this.connectionDistance) {
                    const lineOpacity = (1 - distance / this.connectionDistance) * 0.2;
                    this.ctx.beginPath();
                    this.ctx.moveTo(p.x, p.y);
                    this.ctx.lineTo(p2.x, p2.y);
                    this.ctx.strokeStyle = hexToRgba(p.color, lineOpacity);
                    this.ctx.lineWidth = 0.5;
                    this.ctx.stroke();
                }
            }
        });

        requestAnimationFrame(() => this.animate());
    }
}

// ========================================
// 📄 PAGE NAVIGATION
// ========================================

let currentPage = 'home';

function initNavigation() {
    const navLinks = document.querySelectorAll('.nav-link');
    const ctaButtons = document.querySelectorAll('[data-page]');

    function navigateToPage(pageId) {
        if (pageId === currentPage) return;

        const currentSection = document.getElementById(`page-${currentPage}`);
        const nextSection = document.getElementById(`page-${pageId}`);

        if (!nextSection) return;

        // Fade out current page
        currentSection.classList.add('fade-out');

        setTimeout(() => {
            currentSection.classList.remove('active', 'fade-out');

            // Fade in next page
            nextSection.classList.add('active');

            // Update nav
            navLinks.forEach(link => {
                link.classList.toggle('active', link.dataset.page === pageId);
            });

            currentPage = pageId;

            // Re-init reveal animations
            initScrollReveal();

            // Animer les barres de compétences si on navigue vers Skills
            if (pageId === 'skills') {
                setTimeout(() => animerBarresCompetences(), 400);
            }

            // Animer stats + typewriter si on revient vers Home
            if (pageId === 'home') {
                setTimeout(() => {
                    initTypewriter();
                    animerStats();
                }, 400);
            }

            // Scroll to top
            window.scrollTo({ top: 0, behavior: 'smooth' });

        }, 300);
    }

    // Nav links
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            navigateToPage(link.dataset.page);
        });
    });

    // CTA buttons
    ctaButtons.forEach(btn => {
        if (!btn.classList.contains('nav-link')) {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                navigateToPage(btn.dataset.page);
            });
        }
    });
}

// ========================================
// 📜 SCROLL REVEAL ANIMATIONS
// ========================================

function initScrollReveal() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('active');
            }
        });
    }, { threshold: 0.1 });

    document.querySelectorAll('.reveal').forEach(el => {
        el.classList.remove('active');
        observer.observe(el);
    });
}

// ========================================
// 📊 ANIMATION BARRES COMPÉTENCES
// ========================================

function animerBarresCompetences() {
    const barres = document.querySelectorAll('.skill-bar__fill');
    barres.forEach((barre, index) => {
        const niveau = barre.getAttribute('data-level');
        setTimeout(() => {
            barre.style.width = niveau + '%';
        }, 100 + index * 30);
    });
}

// ========================================
// 🖥️ DYNAMIC RENDERING
// ========================================

function renderHeroBadges() {
    const container = document.getElementById('hero-badges');
    if (!container) return;

    container.innerHTML = HERO_BADGES.map(b => `
        <span class="hero-badge hero-badge--${b.color}">
            <span class="hero-badge__icon">${b.icone}</span>
            ${b.label}
        </span>
    `).join('');
}

// ========================================
// ⌨️ TYPEWRITER EFFECT
// ========================================

function initTypewriter() {
    const el = document.getElementById('hero-typewriter');
    if (!el) return;

    // Stop any previous typewriter
    if (window._typewriterTimer) clearTimeout(window._typewriterTimer);

    const phrases = [
        'Futur Analyste GRC',
        'Chef d\'Entreprise actif',
        'Passionné de Cybersécurité'
    ];

    let phraseIdx = 0, charIdx = 0, deleting = false;

    function type() {
        const current = phrases[phraseIdx];
        if (!deleting) {
            el.textContent = current.slice(0, ++charIdx);
            if (charIdx === current.length) {
                deleting = true;
                window._typewriterTimer = setTimeout(type, 2000);
                return;
            }
        } else {
            el.textContent = current.slice(0, --charIdx);
            if (charIdx === 0) {
                deleting = false;
                phraseIdx = (phraseIdx + 1) % phrases.length;
            }
        }
        window._typewriterTimer = setTimeout(type, deleting ? 50 : 80);
    }
    type();
}

// ========================================
// 📊 ANIMATED STATS COUNTER
// ========================================

function animerStats() {
    document.querySelectorAll('.hero-stat__value').forEach(el => {
        const target = parseInt(el.getAttribute('data-target'));
        let current = 0;
        const step = Math.ceil(target / 40);
        const timer = setInterval(() => {
            current = Math.min(current + step, target);
            el.textContent = current;
            if (current >= target) clearInterval(timer);
        }, 40);
    });
}

function renderProjects() {
    const container = document.getElementById('projects-grid');
    if (!container) return;

    container.innerHTML = MES_PROJETS.map((projet, i) => `
        <div class="project-card reveal" style="transition-delay: ${i * 0.1}s">
            <div class="project-icon">
                <span class="project-icon-emoji">${projet.icone}</span>
            </div>
            <h3 class="project-title">${projet.titre}</h3>
            <p class="project-description">${projet.description}</p>
            <div class="project-tags">
                ${projet.tags.map(tag => `<span class="tag">${tag}</span>`).join('')}
            </div>
            <a href="${projet.lien}" target="_blank" rel="noopener noreferrer" class="project-link">
                <i class="fab fa-github"></i> Code Source
                <i class="fas fa-arrow-right"></i>
            </a>
            <span class="project-date">${projet.date}</span>
        </div>
    `).join('');
}

function renderSkills() {
    const container = document.getElementById('skills-grid');
    if (!container) return;

    container.innerHTML = MES_COMPETENCES.map((cat, i) => `
        <div class="skills-category skills-category--${cat.couleur} reveal" style="transition-delay: ${i * 0.1}s">
            <h3 class="skills-category__title">
                <i class="${cat.icone}"></i> ${cat.categorie}
            </h3>
            <div class="skills-list">
                ${cat.items.map(item => `
                    <div class="skill-item-row">
                        <div class="skill-item__header">
                            <span class="skill-item__name">${item.nom}</span>
                            ${item.badge ? `<span class="skill-badge">${item.badge}</span>` : ''}
                            <span class="skill-item__level">${item.niveau}%</span>
                        </div>
                        <div class="skill-bar">
                            <div class="skill-bar__fill skill-bar__fill--${cat.couleur}" 
                                 style="width: 0%" 
                                 data-level="${item.niveau}">
                            </div>
                        </div>
                    </div>
                `).join('')}
            </div>
        </div>
    `).join('');
}

function renderContact() {
    const container = document.getElementById('contact-grid');
    if (!container) return;

    const info = INFOS_CONTACT;

    container.innerHTML = `
        <div class="contact-info reveal">
            <h2 class="contact-title">Restons en contact</h2>
            <p class="contact-intro">${info.intro}</p>
            
            <div class="contact-details">
                <div class="contact-item">
                    <i class="fas fa-envelope"></i>
                    <span>${info.email}</span>
                </div>
                <div class="contact-item">
                    <i class="fas fa-map-marker-alt"></i>
                    <span>${info.localisation}</span>
                </div>
                <div class="contact-item">
                    <i class="fas fa-briefcase"></i>
                    <span>${info.disponibilite}</span>
                </div>
            </div>
            
            <div class="social-links">
                ${info.reseaux.map(r => `
                    <a href="${r.url}" target="_blank" class="social-btn" title="${r.nom}">
                        <i class="${r.icone}"></i>
                    </a>
                `).join('')}
            </div>
            
            <div class="ctf-section">
                <h4>CTF & Profils</h4>
                <div class="ctf-links">
                    ${info.ctf.map(c => `
                        <a href="${c.url}" target="_blank" class="ctf-link">
                            <i class="${c.icone}"></i>
                            <span>${c.texte}</span>
                            <i class="fas fa-arrow-right arrow"></i>
                        </a>
                    `).join('')}
                </div>
            </div>
            
            <div class="cv-download-section">
                <a href="assets/documents/CV_Poncelet_Dorian.pdf" download class="cv-download-btn">
                    <i class="fas fa-file-pdf"></i>
                    <span>Télécharger mon CV</span>
                    <i class="fas fa-download"></i>
                </a>
            </div>
        </div>
        
        <div class="contact-form-card reveal reveal-delay-1">
            <form id="contact-form">
                <input type="hidden" name="_subject" value="Nouveau message depuis le Portfolio">
                <input type="hidden" name="_captcha" value="false">
                <div class="form-group">
                    <input type="text" name="name" placeholder="Nom complet" required>
                </div>
                <div class="form-group">
                    <input type="email" name="email" placeholder="Email" required>
                </div>
                <div class="form-group">
                    <input type="text" name="subject" placeholder="Sujet" required>
                </div>
                <div class="form-group">
                    <textarea name="message" placeholder="Votre message..." rows="5" required></textarea>
                </div>
                <button type="submit" class="form-btn" id="submit-btn">
                    <i class="fas fa-paper-plane"></i>
                    <span>Envoyer le message</span>
                </button>
            </form>
            <div class="form-footer">
                <i class="fas fa-shield-alt"></i>
                <span>Vos données ne seront jamais partagées avec des tiers.</span>
            </div>
        </div>
    `;

    // Form handler with mailto
    const form = document.getElementById('contact-form');
    if (form) {
        form.addEventListener('submit', (e) => {
            e.preventDefault();

            const submitBtn = document.getElementById('submit-btn');
            const originalHTML = submitBtn.innerHTML;

            // Récupérer les valeurs
            const nom = form.querySelector('input[name="name"]').value;
            const sujet = form.querySelector('input[name="subject"]').value;
            const message = form.querySelector('textarea[name="message"]').value;

            // Construire le lien mailto
            const mailtoLink = `mailto:Dow@ikmail.com?subject=${encodeURIComponent(sujet + ' - Message de ' + nom)}&body=${encodeURIComponent(message)}`;
            window.location.href = mailtoLink;

            // Feedback visuel
            submitBtn.innerHTML = '<i class="fas fa-check-circle"></i> <span>Redirection vers votre client email...</span>';
            submitBtn.disabled = true;
            showToast('✅ Redirection vers votre client email !');

            setTimeout(() => {
                submitBtn.innerHTML = originalHTML;
                submitBtn.disabled = false;
            }, 3000);
        });
    }
}

// ========================================
// 📰 CYBER NEWS RENDERING
// ========================================

async function renderCyberNews() {
    const newsGrid = document.getElementById('cyber-news-grid');
    const audioPlayer = document.getElementById('cyber-audio-player');
    const audioFallback = document.getElementById('audio-fallback');
    const updateDate = document.getElementById('cyber-update-date');
    const scriptSection = document.getElementById('cyber-script-section');
    const scriptContent = document.getElementById('cyber-script-content');

    if (!newsGrid) return;

    try {
        // Fetch local data.json with cache busting
        const cacheBuster = new Date().getTime();
        const response = await fetch(`./cyber-news/data.json?t=${cacheBuster}`);

        if (!response.ok) {
            throw new Error('Données non disponibles');
        }

        const data = await response.json();

        // DEV LOGS - Cyber Pulse Pipeline
        console.log('🛡️ [CyberPulse] Données chargées avec succès');
        console.log('📅 [CyberPulse] Dernière MAJ:', data.generated_at);
        console.log('📰 [CyberPulse] Articles récupérés:', data.articles?.length || 0);
        if (data.script) console.log('🎙️ [CyberPulse] Script radio disponible');
        if (data.audio_file) console.log('🔊 [CyberPulse] Audio briefing:', data.audio_file);

        // Update date
        if (updateDate && data.generated_at) {
            const date = new Date(data.generated_at);
            updateDate.textContent = `Dernière mise à jour : ${date.toLocaleDateString('fr-FR')} à ${date.toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })}`;
        }

        // 🎵 FORCE AUDIO UPDATE (Cache Busting)
        if (data.audio_file && audioPlayer) {
            // Construit le chemin avec un timestamp pour éviter le cache navigateur
            // data.audio_file est relatif (ex: "audio/latest_briefing.mp3")
            const audioPath = `./cyber-news/${data.audio_file}?t=${new Date().getTime()}`;
            console.log('🔊 [CyberPulse] Updating audio source:', audioPath);

            audioPlayer.src = audioPath;
            audioPlayer.load(); // Force le rechargement du flux
        }

        // Render articles
        if (data.articles && data.articles.length > 0) {
            newsGrid.innerHTML = data.articles.map((article, index) => `
                <article class="cyber-news-item reveal" style="transition-delay: ${index * 0.1}s">
                    <span class="news-item-index">[${String(index + 1).padStart(2, '0')}]</span>
                    <h3 class="news-item-title">
                        <a href="${article.url}" target="_blank" rel="noopener noreferrer">
                            ${article.title_fr || article.title}
                        </a>
                    </h3>
                    <p class="news-item-summary">${article.summary_fr || article.summary}</p>
                    <a href="${article.url}" target="_blank" rel="noopener noreferrer" class="news-item-link">
                        <i class="fas fa-external-link-alt"></i> Lire l'article
                    </a>
                </article>
            `).join('');

            // Re-init reveal animations
            initScrollReveal();
        } else {
            newsGrid.innerHTML = `
                <div class="cyber-error">
                    <i class="fas fa-database"></i>
                    <p>Aucune actualité disponible pour le moment</p>
                </div>
            `;
        }

        // Display script if available
        if (scriptSection && scriptContent && data.script) {
            const scriptRadio = data.script && data.script.trim().length > 50
                ? data.script
                : "\u26a0\ufe0f Script radio non disponible pour cette session. Consultez les articles ci-dessous.";
            scriptSection.style.display = 'block';
            scriptContent.textContent = scriptRadio;
        }

    } catch (error) {
        console.error('Erreur chargement Cyber News:', error);
        newsGrid.innerHTML = `
            <div class="cyber-error">
                <i class="fas fa-exclamation-triangle"></i>
                <p>Impossible de charger les actualités</p>
                <p style="font-size: 0.8rem; margin-top: 0.5rem; opacity: 0.7;">${error.message}</p>
            </div>
        `;
    }

    // Handle audio fallback
    if (audioPlayer) {
        audioPlayer.addEventListener('error', () => {
            const customPlayer = document.getElementById('custom-audio-player');
            if (customPlayer) customPlayer.style.display = 'none';
            if (audioFallback) {
                audioFallback.style.display = 'flex';
            }
        });

        // Initialize custom audio player
        initCustomAudioPlayer();
    }
}

// ========================================
// 🎵 CUSTOM AUDIO PLAYER
// ========================================

function initCustomAudioPlayer() {
    const audio = document.getElementById('cyber-audio-player');
    const playBtn = document.getElementById('audio-play-btn');
    const playIcon = document.getElementById('play-icon');
    const progressBar = document.getElementById('audio-progress-bar');
    const progress = document.getElementById('audio-progress');
    const progressHandle = document.getElementById('audio-progress-handle');
    const currentTimeEl = document.getElementById('audio-current-time');
    const durationEl = document.getElementById('audio-duration');
    const volumeBtn = document.getElementById('audio-volume-btn');
    const volumeIcon = document.getElementById('volume-icon');
    const volumeSlider = document.getElementById('audio-volume-slider');
    const volumeLevel = document.getElementById('volume-level');
    const visualizer = document.getElementById('audio-visualizer');

    if (!audio || !playBtn) return;

    // Format time helper
    function formatTime(seconds) {
        if (isNaN(seconds)) return '0:00';
        const mins = Math.floor(seconds / 60);
        const secs = Math.floor(seconds % 60);
        return `${mins}:${secs.toString().padStart(2, '0')}`;
    }

    // Play/Pause toggle
    playBtn.addEventListener('click', () => {
        if (audio.paused) {
            audio.play();
            playIcon.className = 'fas fa-pause';
            visualizer.classList.add('playing');
        } else {
            audio.pause();
            playIcon.className = 'fas fa-play';
            visualizer.classList.remove('playing');
        }
    });

    // Update progress bar
    audio.addEventListener('timeupdate', () => {
        const percent = (audio.currentTime / audio.duration) * 100;
        progress.style.width = `${percent}%`;
        progressHandle.style.left = `${percent}%`;
        currentTimeEl.textContent = formatTime(audio.currentTime);
    });

    // Set duration when loaded
    audio.addEventListener('loadedmetadata', () => {
        durationEl.textContent = formatTime(audio.duration);
    });

    // Handle audio end
    audio.addEventListener('ended', () => {
        playIcon.className = 'fas fa-play';
        visualizer.classList.remove('playing');
        progress.style.width = '0%';
        progressHandle.style.left = '0%';
    });

    // Click on progress bar to seek
    progressBar.addEventListener('click', (e) => {
        const rect = progressBar.getBoundingClientRect();
        const percent = (e.clientX - rect.left) / rect.width;
        audio.currentTime = percent * audio.duration;
    });

    // Volume control
    let currentVolume = 0.7;
    audio.volume = currentVolume;
    volumeLevel.style.width = `${currentVolume * 100}%`;

    volumeBtn.addEventListener('click', () => {
        if (audio.volume > 0) {
            audio.volume = 0;
            volumeLevel.style.width = '0%';
            volumeIcon.className = 'fas fa-volume-mute';
        } else {
            audio.volume = currentVolume;
            volumeLevel.style.width = `${currentVolume * 100}%`;
            volumeIcon.className = 'fas fa-volume-up';
        }
    });

    volumeSlider.addEventListener('click', (e) => {
        const rect = volumeSlider.getBoundingClientRect();
        const percent = Math.max(0, Math.min(1, (e.clientX - rect.left) / rect.width));
        audio.volume = percent;
        currentVolume = percent;
        volumeLevel.style.width = `${percent * 100}%`;

        if (percent === 0) {
            volumeIcon.className = 'fas fa-volume-mute';
        } else if (percent < 0.5) {
            volumeIcon.className = 'fas fa-volume-down';
        } else {
            volumeIcon.className = 'fas fa-volume-up';
        }
    });
}

// ========================================
// 🍞 TOAST NOTIFICATION
// ========================================

function showToast(message = 'Action effectuée !') {
    const toast = document.getElementById('toast');
    if (toast) {
        toast.querySelector('span').textContent = message;
        toast.classList.add('show');
        setTimeout(() => toast.classList.remove('show'), 3000);
    }
}

// ========================================
// ✨ CARD SPOTLIGHT EFFECT
// ========================================

function initSpotlightEffect() {
    document.querySelectorAll('.project-card, .skill-category').forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            card.style.setProperty('--mouse-x', `${x}px`);
            card.style.setProperty('--mouse-y', `${y}px`);
        });
    });
}

// ========================================
// 🚀 INITIALIZATION
// ========================================

document.addEventListener('DOMContentLoaded', () => {
    // Initialize particle system
    const canvas = document.getElementById('particles-canvas');
    if (canvas) {
        new ParticleSystem(canvas);
    }

    // Render all sections
    renderHeroBadges();
    renderProjects();
    renderSkills();
    renderContact();
    renderCyberNews();

    // Initialize hero animations
    initTypewriter();
    animerStats();

    // Initialize interactions
    initNavigation();
    initScrollReveal();
    initSpotlightEffect();

    // Initial reveal
    setTimeout(() => {
        document.querySelectorAll('#page-home .reveal, #page-home .hero-stat, #page-home .hero-badge').forEach(el => {
            el.classList.add('active');
        });
    }, 100);

    console.log('🚀 Vision 2026 Multi-Page Portfolio Loaded');
});
