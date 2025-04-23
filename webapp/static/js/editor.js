/**
 * Coding Challenge Editor
 * 
 * Dieses Skript initialisiert den Monaco-Editor und die Funktionen zum
 * Ausführen und Einreichen von Code.
 */

document.addEventListener('DOMContentLoaded', function() {
    // Nur initialisieren, wenn Editor-Element vorhanden ist
    if (!document.getElementById('editor')) return;

    // Variablen aus HTML-Datenattributen auslesen
    const editorElement = document.getElementById('editor');
    const challengeId = editorElement.dataset.challengeId || 0;
    const startCode = editorElement.dataset.starterCode || '';
    
    let editor;
    
    // Editor initialisieren
    require.config({ paths: { 'vs': 'https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.34.0/min/vs' } });
    
    require(['vs/editor/editor.main'], function () {
        // Editor erstellen
        editor = monaco.editor.create(document.getElementById('editor'), {
            value: startCode,
            language: 'python',
            theme: 'vs-light',
            fontSize: 14,
            minimap: { enabled: false },
            automaticLayout: true
        });

        // Themes definieren
        initializeThemes();
        
        // Theme-Auswahl aktivieren
        document.getElementById('themeSelect').addEventListener('change', function () {
            const newTheme = this.value;
            monaco.editor.setTheme(newTheme);
        });
    });

    // Code ausführen
    window.runCode = function() {
        if (!editor) return;
        
        const code = editor.getValue();

        fetch("/run", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ code: code })
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById("output-text").textContent = data.output;
        })
        .catch(err => {
            document.getElementById("output-text").textContent = "❌ Fehler beim Ausführen.";
            console.error(err);
        });
    };

    // Code einreichen
    window.submitCode = function() {
        if (!editor) return;
        
        const code = editor.getValue();
        const discordUsername = document.getElementById("discordUsername").value;
        
        // Ergebnis-Container zurücksetzen
        const resultContainer = document.getElementById("result-container");
        resultContainer.style.display = "none";
        resultContainer.classList.remove("result-success", "result-error");
        
        // Zeige Ladeindikator
        document.getElementById("output-text").textContent = "Prüfe Lösung und sende an Discord...";
        
        fetch("/submit", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ 
                code: code,
                challenge_id: challengeId,
                discord_username: discordUsername
            })
        })
        .then(response => response.json())
        .then(data => {
            // Ergebnis anzeigen
            resultContainer.style.display = "block";
            
            if (data.status === "success") {
                resultContainer.classList.add("result-success");
                document.getElementById("result-title").textContent = "✅ " + data.message;
            } else {
                resultContainer.classList.add("result-error");
                document.getElementById("result-title").textContent = "❌ " + data.message;
            }
            
            // Details anzeigen
            if (data.details) {
                let detailsHtml = "<ul>";
                data.details.forEach(detail => {
                    const status = detail.passed ? "✅" : "❌";
                    detailsHtml += `<li>${status} ${detail.test} → Erwartet: ${detail.expected}, Erhielt: ${detail.actual}</li>`;
                });
                detailsHtml += "</ul>";
                document.getElementById("result-details").innerHTML = detailsHtml;
            } else {
                document.getElementById("result-details").textContent = "";
            }
            
            // Wenn Discord-Username angegeben wurde
            if (discordUsername) {
                if (data.discord_notification) {
                    document.getElementById("result-details").innerHTML += 
                        `<div class="alert alert-success mt-3">
                            <strong>✅ Discord-Benachrichtigung</strong>: Das Ergebnis wurde an Discord gesendet (Benutzer: ${discordUsername})
                        </div>`;
                } else {
                    document.getElementById("result-details").innerHTML += 
                        `<div class="alert alert-warning mt-3">
                            <strong>⚠️ Hinweis</strong>: Die Discord-Benachrichtigung konnte nicht gesendet werden. 
                            Der Server ist möglicherweise nicht richtig konfiguriert.
                        </div>`;
                }
            } else if (data.status === "success") {
                document.getElementById("result-details").innerHTML += 
                    `<div class="alert alert-info mt-3">
                        <strong>💡 Tipp</strong>: Gib deinen Discord-Namen ein, um dein Ergebnis im Discord-Channel zu teilen!
                    </div>`;
            }
        })
        .catch(err => {
            resultContainer.style.display = "block";
            resultContainer.classList.add("result-error");
            document.getElementById("result-title").textContent = "❌ Fehler beim Einreichen";
            document.getElementById("result-details").textContent = "Bitte versuche es später erneut.";
            console.error(err);
        });
    };

    // Editor-Themes initialisieren
    function initializeThemes() {
        monaco.editor.defineTheme('dracula', {
            base: 'vs-dark',
            inherit: true,
            rules: [
                { token: '', background: '282a36', foreground: 'f8f8f2' },
                { token: 'comment', foreground: '6272a4' },
                { token: 'keyword', foreground: 'ff79c6' },
                { token: 'string', foreground: 'f1fa8c' }
            ],
            colors: { 'editor.background': '#282a36' }
        });

        monaco.editor.defineTheme('solarized-light', {
            base: 'vs',
            inherit: true,
            rules: [
                { token: '', foreground: '586e75', background: 'fdf6e3' },
                { token: 'comment', foreground: '93a1a1' },
                { token: 'keyword', foreground: '859900' },
                { token: 'string', foreground: '2aa198' }
            ],
            colors: { 'editor.background': '#fdf6e3' }
        });

        monaco.editor.defineTheme('solarized-dark', {
            base: 'vs-dark',
            inherit: true,
            rules: [
                { token: '', foreground: '839496', background: '002b36' },
                { token: 'comment', foreground: '586e75' },
                { token: 'keyword', foreground: 'cb4b16' },
                { token: 'string', foreground: '2aa198' }
            ],
            colors: { 'editor.background': '#002b36' }
        });

        monaco.editor.defineTheme('github-dark', {
            base: 'vs-dark',
            inherit: true,
            rules: [
                { token: '', foreground: 'c9d1d9', background: '0d1117' },
                { token: 'comment', foreground: '8b949e' },
                { token: 'keyword', foreground: 'ff7b72' },
                { token: 'string', foreground: 'a5d6ff' }
            ],
            colors: { 'editor.background': '#0d1117' }
        });

        monaco.editor.defineTheme('monokai', {
            base: 'vs-dark',
            inherit: true,
            rules: [
                { token: '', foreground: 'f8f8f2', background: '272822' },
                { token: 'comment', foreground: '75715e' },
                { token: 'keyword', foreground: 'f92672' },
                { token: 'string', foreground: 'a6e22e' }
            ],
            colors: { 'editor.background': '#272822' }
        });
    }
}); 