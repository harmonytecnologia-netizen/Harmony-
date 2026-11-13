# Mascote da JPC: "Gabi", um gabinete gamer com rosto (desenho original em SVG)
def gabi(mood="feliz", size=420):
    eyes = {
        "feliz":  '<path d="M118 150 q22 -26 44 0" stroke="#fff" stroke-width="11" fill="none" stroke-linecap="round"/><path d="M198 150 q22 -26 44 0" stroke="#fff" stroke-width="11" fill="none" stroke-linecap="round"/>',
        "alerta": '<circle cx="140" cy="148" r="17" fill="#fff"/><circle cx="220" cy="148" r="17" fill="#fff"/><circle cx="144" cy="150" r="8" fill="#0b0618"/><circle cx="224" cy="150" r="8" fill="#0b0618"/>',
        "triste": '<path d="M118 140 q22 22 44 0" stroke="#fff" stroke-width="11" fill="none" stroke-linecap="round"/><path d="M198 140 q22 22 44 0" stroke="#fff" stroke-width="11" fill="none" stroke-linecap="round"/>',
    }[mood]
    mouth = {
        "feliz":  '<path d="M150 190 q30 32 60 0 z" fill="#ff4fd8"/>',
        "alerta": '<ellipse cx="180" cy="200" rx="18" ry="22" fill="#ff4fd8"/>',
        "triste": '<path d="M150 210 q30 -26 60 0" stroke="#ff4fd8" stroke-width="10" fill="none" stroke-linecap="round"/>',
    }[mood]
    return f'''<svg width="{size}" height="{size*1.25:.0f}" viewBox="0 0 360 450" xmlns="http://www.w3.org/2000/svg">
<defs>
 <linearGradient id="rgb" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#8b5cff"/><stop offset=".5" stop-color="#22d3ee"/><stop offset="1" stop-color="#ff4fd8"/></linearGradient>
 <linearGradient id="vid" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1b1033"/><stop offset="1" stop-color="#0b0618"/></linearGradient>
 <filter id="gl"><feGaussianBlur stdDeviation="6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs>
<ellipse cx="180" cy="432" rx="120" ry="14" fill="#000" opacity=".45"/>
<rect x="40" y="20" width="280" height="400" rx="34" fill="url(#rgb)" filter="url(#gl)"/>
<rect x="52" y="32" width="256" height="376" rx="26" fill="url(#vid)"/>
<g opacity=".9">
 <circle cx="180" cy="300" r="46" fill="none" stroke="url(#rgb)" stroke-width="8"/>
 <circle cx="180" cy="300" r="10" fill="#22d3ee"/>
 <path d="M180 262 q16 22 0 38 q-16 -22 0 -38" fill="#8b5cff" opacity=".8"/>
 <path d="M218 300 q-22 16 -38 0 q22 -16 38 0" fill="#22d3ee" opacity=".8"/>
 <path d="M180 338 q-16 -22 0 -38 q16 22 0 38" fill="#ff4fd8" opacity=".8"/>
 <path d="M142 300 q22 -16 38 0 q-22 16 -38 0" fill="#8b5cff" opacity=".8"/>
</g>
{eyes}
{mouth}
<circle cx="112" cy="196" r="12" fill="#ff4fd8" opacity=".35"/><circle cx="248" cy="196" r="12" fill="#ff4fd8" opacity=".35"/>
<rect x="268" y="48" width="22" height="8" rx="4" fill="#22d3ee"/>
<rect x="8" y="230" width="34" height="18" rx="9" fill="url(#rgb)"/><rect x="318" y="230" width="34" height="18" rx="9" fill="url(#rgb)"/>
</svg>'''
