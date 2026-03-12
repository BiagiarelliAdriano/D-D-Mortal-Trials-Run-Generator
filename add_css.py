css_to_add = """

/* --- Spellcasting Widget --- */
.spellcasting-widget { display: flex; flex-direction: column; gap: 10px; padding: 15px; }
.spellcasting-header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--border-color); padding-bottom: 8px; }
.manage-spells-btn { background: var(--bg-hover); color: var(--text-color); border: 1px solid var(--border-color); padding: 5px 10px; border-radius: 4px; cursor: pointer; transition: 0.2s; font-family: 'Cinzel', serif; font-weight: bold; }
.manage-spells-btn:hover { background: var(--accent-light); color: var(--bg-color); }
.spell-stats-row { display: flex; gap: 10px; justify-content: space-between; }
.spell-stat-box { background: var(--bg-dark); border: 1px solid var(--border-color); padding: 8px 12px; border-radius: 6px; text-align: center; flex: 1; display: flex; flex-direction: column; }
.spell-stat-label { font-size: 0.8rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 1px; }
.spell-stat-val { font-size: 1.2rem; font-weight: bold; color: var(--accent-light); }
.spell-slots-row { display: flex; gap: 8px; flex-wrap: wrap; margin-top: 10px; }
.spell-slot-box { background: var(--bg-dark); border: 1px solid var(--accent-color); padding: 4px 8px; border-radius: 4px; display: flex; align-items: center; gap: 5px; font-size: 0.9rem; }
.slot-lvl { color: var(--text-muted); font-size: 0.8rem; }
.slot-count { font-weight: bold; color: var(--accent-light); text-shadow: 0 0 5px rgba(255,255,255,0.2); }
.prepared-spells-list { flex: 1; display: flex; flex-direction: column; gap: 10px; margin-top: 10px; padding-right: 5px; }
.spell-level-group h4 { margin: 0 0 5px 0; font-size: 1rem; color: var(--gold); border-bottom: 1px dashed var(--border-color); padding-bottom: 3px; font-family: 'Cinzel', serif; }
.prepared-spell-row { display: flex; justify-content: space-between; padding: 6px 10px; background: rgba(0,0,0,0.3); border-radius: 4px; margin-bottom: 4px; font-size: 0.95rem; border-left: 3px solid var(--accent-color); transition: 0.2s; }
.prepared-spell-row:hover { background: rgba(255,255,255,0.05); border-left-color: var(--gold); }
.spell-school { color: var(--text-muted); font-size: 0.8rem; font-style: italic; }

/* --- Spell Selection Overlay --- */
.spell-overlay { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(0, 0, 0, 0.7); backdrop-filter: blur(8px); z-index: 9999; display: flex; align-items: center; justify-content: center; animation: fadeIn 0.2s ease-out; }
.spell-overlay-content { width: 75%; height: 85%; background: var(--bg-color); border: 2px solid var(--accent-light); border-radius: 12px; display: flex; flex-direction: column; box-shadow: 0 15px 50px rgba(0,0,0,0.8); overflow: hidden; animation: slideUp 0.3s ease-out; }
.overlay-header { display: flex; justify-content: space-between; align-items: center; padding: 15px 25px; background: var(--bg-dark); border-bottom: 1px solid var(--border-color); }
.overlay-header h2 { margin: 0; color: var(--accent-light); text-shadow: 0 0 10px rgba(255,255,255,0.3); font-family: 'Cinzel', serif; }
.overlay-hint { padding: 10px 25px; margin: 0; font-style: italic; color: var(--text-muted); border-bottom: 1px solid rgba(255,255,255,0.05); font-size: 0.9rem; background: rgba(0,0,0,0.2); }
.spell-overlay-list { flex: 1; overflow-y: auto; padding: 20px 25px; display: flex; flex-direction: column; gap: 20px; }
.overlay-level-group h3 { margin: 0 0 10px 0; color: var(--gold); border-bottom: 1px solid var(--border-color); padding-bottom: 5px; font-family: 'Cinzel', serif; font-size: 1.3rem; }
.spell-selection-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 12px; }
.spell-select-card { background: var(--bg-dark); border: 1px solid var(--border-color); border-radius: 6px; padding: 12px; cursor: pointer; transition: all 0.2s; position: relative; user-select: none; }
.spell-select-card:hover { border-color: var(--accent-light); transform: translateY(-2px); box-shadow: 0 4px 10px rgba(0,0,0,0.3); background: rgba(255,255,255,0.03); }
.spell-select-card.selected { background: rgba(0, 180, 255, 0.1); border-color: var(--accent-light); box-shadow: inset 0 0 10px rgba(0, 180, 255, 0.1); }
.spell-name { font-weight: bold; margin-bottom: 4px; font-size: 1.05rem; }
.spell-check { position: absolute; top: 10px; right: 10px; color: var(--accent-light); font-weight: bold; font-size: 1.2rem; text-shadow: 0 0 5px rgba(255,255,255,0.5); }
.no-slots-msg, .no-spells-note { font-style: italic; color: var(--text-muted); font-size: 0.9rem; padding: 10px 0; }
"""

filepath = r"d:\rungenerator\D-D-Mortal-Trials-Run-Generator\frontend\src\styles\CharacterSheet.css"
with open(filepath, 'a', encoding='utf-8') as f:
    f.write(css_to_add)

print("CSS appended successfully.")
