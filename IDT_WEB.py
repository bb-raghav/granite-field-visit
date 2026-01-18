# app.py
# Hybrid Python + HTML + CSS desktop/web app for Granite Field Visit — Expanded Gallery + Interactive Info Cards
# Run: pip install flask
# Then: python app.py  -> open http://127.0.0.1:8888

from flask import Flask, render_template_string, url_for
import os

app = Flask(__name__)
BASE = os.path.dirname(__file__)
STATIC = os.path.join(BASE, 'static')
GALLERY = os.path.join(STATIC, 'gallery')
MACHINES = os.path.join(STATIC, 'machines')
SAFETY = os.path.join(STATIC, 'safety')
REPORTS = os.path.join(STATIC, 'reports')
for p in (GALLERY, MACHINES, SAFETY, REPORTS): os.makedirs(p, exist_ok=True)

TEMPLATE = """
<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
  <title>Team Phantom — Granite Field Visit</title>
  <link href=\"https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800;900&display=swap\" rel=\"stylesheet\">
  <style>
    :root{--bg:#0b1220;--panel:#0f172a;--card:#0f1b34;--muted:#9aa6c3;--fg:#e9ecf5;--acc:#f97316;--acc2:#22d3ee;--acc3:#a78bfa;--r:18px;--sh:0 20px 50px rgba(0,0,0,.45)}
    *{box-sizing:border-box}
    body{margin:0;font-family:Inter;background:radial-gradient(1200px 600px at 80% -10%,rgba(34,211,238,.18),transparent 40%),radial-gradient(900px 500px at -10% 10%,rgba(249,115,22,.22),transparent 45%),var(--bg);color:var(--fg)}
    .app{display:grid;grid-template-columns:280px 1fr;height:100vh}
    aside{padding:28px;border-right:1px solid #0f172a;background:linear-gradient(180deg,#0b1220,#0a1022)}
    .brand{font-weight:900;font-size:22px}
    .sub{color:var(--muted);margin-top:6px}
    nav{margin-top:28px;display:grid;gap:10px}
    nav button{all:unset;cursor:pointer;padding:14px 16px;border-radius:14px;border:1px solid #142042;background:linear-gradient(180deg,#0f172a,#0b1220)}
    nav button.active,nav button:hover{border-color:var(--acc2);box-shadow:0 0 0 1px rgba(34,211,238,.35) inset}
    main{padding:40px;overflow:auto}
    h1{font-size:56px;line-height:1.05;margin:14px 0}
    h2{margin:0 0 12px}
    .pill{display:inline-block;padding:8px 12px;border-radius:999px;background:linear-gradient(135deg,rgba(249,115,22,.2),rgba(34,211,238,.2));border:1px solid rgba(34,211,238,.45)}
    .subtitle{color:var(--acc3);font-weight:800;letter-spacing:.3px}
    .grid{max-width:1100px;margin:28px auto;display:grid;grid-template-columns:repeat(3,1fr);gap:20px}
    .card{background:linear-gradient(180deg,#101c3a,#0b132a);border:1px solid #1a2b55;border-radius:var(--r);padding:22px;box-shadow:var(--sh);position:relative;overflow:hidden}
    .card:before{content:"";position:absolute;inset:auto -40% -60% -40%;height:140px;background:radial-gradient(closest-side,rgba(34,211,238,.18),transparent 70%)}
    .card h3{margin:0 0 8px}
    .muted{color:var(--muted)}

    /* Gallery */
    .tabs{display:flex;gap:10px;margin:10px 0 18px}
    .tabs button{all:unset;cursor:pointer;padding:10px 14px;border-radius:999px;border:1px solid #1a2b55}
    .tabs button.active{background:linear-gradient(135deg,rgba(249,115,22,.25),rgba(34,211,238,.25));border-color:var(--acc2)}
    .gallery{max-width:1100px;margin:28px auto;display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:18px}
    .gallery img{width:100%;aspect-ratio:4/3;object-fit:cover;border-radius:16px;border:1px solid #1a2b55;box-shadow:var(--sh);cursor:zoom-in}

    .map-wrap{border-radius:18px;overflow:hidden;border:1px solid #1a2b55;box-shadow:var(--sh);margin-top:16px}
    footer{max-width:1100px;margin:40px auto;color:var(--muted)}
    @media (max-width:980px){.grid{grid-template-columns:1fr}}
    .lightbox{position:fixed;inset:0;background:rgba(3,7,18,.85);backdrop-filter:blur(4px);display:none;align-items:center;justify-content:center;z-index:999}
    .lightbox.open{display:flex}
    .lightbox img{max-width:92vw;max-height:92vh;border-radius:18px;box-shadow:0 30px 80px rgba(0,0,0,.8)}
    .lightbox .close{position:absolute;top:18px;right:22px;font-size:28px;cursor:pointer;color:#fff}
  </style>
</head>
<body>
<div class=\"app\">
  <aside>
    <div class=\"brand\">Team Phantom</div>
    <div class=\"sub\">Granite Manufacturing Field Visit</div>
    <nav>
      <button class=\"active\" data-tab=\"overview\">Overview</button>
      <button data-tab=\"problems\">Problems</button>
      <button data-tab=\"solutions\">Solutions</button>
      <button data-tab=\"gallery\">Gallery</button>
      <button data-tab=\"tech\">Machines & Tech</button>
      <button data-tab=\"safety\">Health & Safety</button>
      <button data-tab=\"report\">Report</button>
      <button data-tab=\"location\">Location</button>
      <button data-tab=\"team\">Team</button>
    </nav>
  </aside>
  <main>
    <section id=\"overview\">
      <span class=\"pill\">Team Phantom • Field Study 2024</span>
      <div class=\"subtitle\">IDT Field Trip</div>
      <h1>Inside a Granite Manufacturing Shop</h1>
      <p class=\"muted\" style=\"max-width:760px\">A technical field study documenting engineering challenges and solutions in granite cutting — silica dust exposure, heavy material handling, water management, and the economics of diamond‑tipped machinery.</p>
      <div class=\"grid\">
        <div class=\"card\"><h3>Why It Matters</h3><p class=\"muted\">Silicosis is a preventable occupational disease. Engineering controls reduce exposure by >90% when correctly implemented.</p></div>
        <div class=\"card\"><h3>What We Observed</h3><p class=\"muted\">Dry cutting, inconsistent PPE, manual slab handling, open slurry disposal, and high downtime from blade wear.</p></div>
        <div class=\"card\"><h3>Our Goal</h3><p class=\"muted\">Design a safer, cleaner, and more productive workflow using proven engineering controls and automation.</p></div>
      </div>
    </section>

    <section id=\"problems\" hidden>
      <h2>Problems Observed</h2>
      <div class=\"grid\">
        <div class=\"card\"><h3>Silica Dust Exposure</h3><p class=\"muted\">Respirable crystalline silica from dry cutting causes silicosis, COPD and lung cancer. Lack of LEV and poor respirator use increase risk.</p></div>
        <div class=\"card\"><h3>Unsafe Lifting</h3><p class=\"muted\">400–1000 lb slabs moved manually cause musculoskeletal injuries and crushing hazards.</p></div>
        <div class=\"card\"><h3>Water & Slurry Disposal</h3><p class=\"muted\">Open slurry dumping clogs drains and contaminates soil, risking regulatory action.</p></div>
        <div class=\"card\"><h3>Noise & Vibration</h3><p class=\"muted\">>95 dB exposure leads to hearing loss and fatigue without protection.</p></div>
        <div class=\"card\"><h3>Blade Wear & Downtime</h3><p class=\"muted\">Variable hardness causes uneven wear, frequent blade changes, and lost production time.</p></div>
        <div class=\"card\"><h3>Electrical Safety</h3><p class=\"muted\">Exposed wiring near water with no RCD protection increases shock hazard.</p></div>
      </div>
    </section>

    <section id=\"solutions\" hidden>
      <h2>Engineering Solutions</h2>
      <div class=\"grid\">
        <div class=\"card\"><h3>Local Exhaust Ventilation (LEV)</h3><p class=\"muted\">Shrouds + HEPA vacuums capture dust at the source, reducing exposure by up to 90%.</p></div>
        <div class=\"card\"><h3>Wet Cutting Systems</h3><p class=\"muted\">Integrated water delivery suppresses dust and cools blades, extending life.</p></div>
        <div class=\"card\"><h3>Ergonomic Automation</h3><p class=\"muted\">Vacuum lifters and roller conveyors remove manual lifting and improve throughput.</p></div>
        <div class=\"card\"><h3>Closed‑Loop Water Filtration</h3><p class=\"muted\">Sedimentation tanks recycle 95% of water and dewater sludge for compliant disposal.</p></div>
        <div class=\"card\"><h3>Predictive Maintenance</h3><p class=\"muted\">Wear sensors + scheduling reduce blade cost and downtime.</p></div>
        <div class=\"card\"><h3>Electrical Safety Upgrades</h3><p class=\"muted\">RCD breakers, waterproof enclosures, and proper earthing prevent shocks.</p></div>
      </div>
    </section>

    <section id=\"gallery\" hidden>
      <h2>Gallery</h2>
      <div class=\"tabs\">
        <button class=\"active\" data-g=\"all\">All</button>
        <button data-g=\"trip\">Trip Photos</button>
        <button data-g=\"machines\">Machines</button>
        <button data-g=\"safety\">Safety Posters</button>
      </div>
      <div class=\"gallery\" id=\"galleryGrid\">
        {% for img in trip %}<img data-cat=\"trip\" src=\"{{ url_for('static', filename='gallery/'+img) }}\" onclick=\"openLightbox(this.src)\">{% endfor %}
        {% for img in machines %}<img data-cat=\"machines\" src=\"{{ url_for('static', filename='machines/'+img) }}\" onclick=\"openLightbox(this.src)\">{% endfor %}
        {% for img in safety %}<img data-cat=\"safety\" src=\"{{ url_for('static', filename='safety/'+img) }}\" onclick=\"openLightbox(this.src)\">{% endfor %}
      </div>
    </section>

    <section id=\"tech\" hidden>
      <h2>Machines & Technology</h2>
      <div class=\"grid\">
        <div class=\"card\"><h3>Bridge Saw</h3><p class=\"muted\">Primary slab cutting machine for straight cuts with high throughput and accuracy.</p></div>
        <div class=\"card\"><h3>CNC Router</h3><p class=\"muted\">Automated profiling, edging, and complex shapes with repeatable precision.</p></div>
        <div class=\"card\"><h3>Diamond Wire Saw</h3><p class=\"muted\">Efficient block cutting with low kerf loss and reduced vibration.</p></div>
        <div class=\"card\"><h3>Water‑Jet Cutter</h3><p class=\"muted\">Cold cutting with minimal dust for intricate designs.</p></div>
        <div class=\"card\"><h3>Vacuum Lifter</h3><p class=\"muted\">Ergonomic handling of heavy slabs to eliminate manual lifting.</p></div>
        <div class=\"card\"><h3>LEV Dust Collector</h3><p class=\"muted\">High‑efficiency capture at the source to protect worker health.</p></div>
      </div>
    </section>

    <section id=\"safety\" hidden>
      <h2>Health, Safety & Regulations</h2>
      <div class=\"grid\">
        <div class=\"card\"><h3>Silicosis Risk</h3><p class=\"muted\">A preventable but deadly lung disease caused by silica dust. Engineering controls are the most effective protection.</p></div>
        <div class=\"card\"><h3>OSHA / BIS Guidance</h3><p class=\"muted\">Wet methods, LEV, and respiratory protection are required to control silica exposure.</p></div>
        <div class=\"card\"><h3>Hearing Conservation</h3><p class=\"muted\">Noise monitoring, ear protection, and equipment enclosures prevent hearing loss.</p></div>
        <div class=\"card\"><h3>Electrical Safety</h3><p class=\"muted\">RCD protection, grounding, and IP‑rated enclosures reduce shock hazards.</p></div>
        <div class=\"card\"><h3>Training & SOPs</h3><p class=\"muted\">Standard operating procedures and regular training reduce incidents.</p></div>
        <div class=\"card\"><h3>Environmental Compliance</h3><p class=\"muted\">Closed‑loop water and proper slurry disposal meet regulatory requirements.</p></div>
      </div>
    </section>

    <section id=\"report\" hidden>
      <h2>Field Visit Report</h2>
      {% if report %}<iframe src=\"{{ url_for('static', filename='reports/'+report) }}\" width=\"100%\" height=\"700\"></iframe>{% else %}<p class=\"muted\">No report uploaded.</p>{% endif %}
    </section>

    <section id=\"location\" hidden>
      <h2>Location</h2>
      <p class=\"muted\">Sri Banashankari Granites, Bengaluru</p>
      <div class=\"map-wrap\"><iframe src=\"https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3890.115429497091!2d77.53202931525087!3d12.909067776639428!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3bae3fb76d780fb7%3A0x13f19030407b65ee!2sSri%20Banashankari%20Granites!5e0!3m2!1sen!2sin!4v1737200000000\" width=\"100%\" height=\"450\" style=\"border:0;\" loading=\"lazy\"></iframe></div>
    </section>

    <section id=\"team\" hidden>
      <h2>Team</h2>
      <div class=\"grid\">
        <div class=\"card\"><h3>Subhransu Nayak</h3><p class=\"muted\">Process observation & safety analysis</p></div>
        <div class=\"card\"><h3>Raghav Bubna</h3><p class=\"muted\">Automation concepts & UI development</p></div>
        <div class=\"card\"><h3>Y Rahul Yadav</h3><p class=\"muted\">Water management & cost analysis</p></div>
      </div>
    </section>

    <footer>© Team Phantom</footer>
  </main>
</div>
<div class=\"lightbox\" id=\"lightbox\" onclick=\"closeLightbox()\"><span class=\"close\">✕</span><img id=\"lightboxImg\"></div>
<script>
const btns=[...document.querySelectorAll('nav button')];const secs=[...document.querySelectorAll('main section')];
btns.forEach(b=>b.onclick=()=>{btns.forEach(x=>x.classList.remove('active'));b.classList.add('active');secs.forEach(s=>s.hidden=true);document.getElementById(b.dataset.tab).hidden=false;
  if(b.dataset.tab==='gallery'){setGalleryFilter('all');}
});

// Gallery filters: show all by default, then filter by category
const filterBtns=[...document.querySelectorAll('.tabs button')];
const grid=document.getElementById('galleryGrid');
function setGalleryFilter(which){
  filterBtns.forEach(x=>x.classList.toggle('active', x.dataset.g===which));
  [...grid.querySelectorAll('img')].forEach(img=>{
    img.style.display = (which==='all' || img.dataset.cat===which) ? '' : 'none';
  });
}
filterBtns.forEach(b=>b.onclick=()=>setGalleryFilter(b.dataset.g));

document.addEventListener('DOMContentLoaded',()=>setGalleryFilter('all'));

function openLightbox(src){const lb=document.getElementById('lightbox');const img=document.getElementById('lightboxImg');img.src=src;lb.classList.add('open');}
function closeLightbox(){document.getElementById('lightbox').classList.remove('open');}
</script>
</body>
</html>
"""

@app.route('/')
def home():
    trip = [f for f in os.listdir(GALLERY) if f.lower().endswith(('png','jpg','jpeg'))]
    machines = [f for f in os.listdir(MACHINES) if f.lower().endswith(('png','jpg','jpeg'))]
    safety = [f for f in os.listdir(SAFETY) if f.lower().endswith(('png','jpg','jpeg'))]
    reports = [f for f in os.listdir(REPORTS) if f.lower().endswith('.pdf')]
    return render_template_string(TEMPLATE, trip=trip, machines=machines, safety=safety, report=(reports[0] if reports else None))

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8888, debug=True)
