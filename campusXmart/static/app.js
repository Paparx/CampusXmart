(function(){
  // Expose a small API and init handlers for pages
function setSelectedCategory(el, categoryId) {

    const hidden = document.getElementById('selectedCategory');
    hidden.value = categoryId;

    // parent container
    const container = el.closest('.category-buttons');

    // remove selected style from all buttons
    container.querySelectorAll('button[data-cat]').forEach(btn => {
        btn.classList.remove('border-primary', 'bg-primary', 'text-white');
        btn.classList.add('bg-white');
    });

    el.classList.remove('bg-white');
    el.classList.add('border-primary', 'bg-primary', 'text-white');
}

  function initSearchSuggestions(){
    const form = document.getElementById('search-form');
    const input = form ? form.querySelector('#search-input') : document.getElementById('search-input');
    const box = form ? form.querySelector('#suggestions') : document.getElementById('suggestions');
    const suggestUrl = form ? form.dataset.suggestUrl : null;
    if(!input || !box || !suggestUrl) return;
    let debounce;
    input.addEventListener('input', ()=>{
      const q = input.value.trim();
      clearTimeout(debounce);
      if(!q){ box.classList.add('hidden'); box.innerHTML=''; return; }
      debounce = setTimeout(()=>{
        fetch(suggestUrl + '?q=' + encodeURIComponent(q))
          .then(r=>r.json())
          .then(data=>{
            const list = (data.suggestions||[]).map(s=>`<a href="${form.dataset.productlistUrl}?q=${encodeURIComponent(s)}" class="block px-4 py-2 text-sm text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-700">${s}</a>`).join('');
            if(!list){ box.classList.add('hidden'); box.innerHTML=''; return; }
            box.innerHTML = list; box.classList.remove('hidden');
          }).catch(()=>{});
      },250);
    });
    document.addEventListener('click', (e)=>{ if(!box.contains(e.target) && e.target !== input) box.classList.add('hidden'); });
  }

  function initHorizontalScroll(){
    const left = document.getElementById('scrollLeft');
    const right = document.getElementById('scrollRight');
    const container = document.getElementById('cardContainer');
    const amount = 200;
    if(!left || !right || !container) return;
    left.addEventListener('click', ()=> container.scrollBy({left:-amount, behavior:'smooth'}));
    right.addEventListener('click', ()=> container.scrollBy({left:amount, behavior:'smooth'}));
  }

  function initProductFilters(){
    // builds query and redirects to productlist URL from data attribute
    const form = document.getElementById('search-form');
    const productlistUrl = form ? form.dataset.productlistUrl : null;
    if(!productlistUrl) return;

    function submitFilters(){
      const params = new URLSearchParams();
      const qEl = document.getElementById('search-input');
      const q = qEl ? qEl.value.trim() : '';
      if(q) params.set('q', q);
      document.querySelectorAll('input[name="category"]:checked').forEach(ch => params.append('category', ch.value));
      const min = document.getElementById('min-price') ? document.getElementById('min-price').value.trim() : '';
      const max = document.getElementById('max-price') ? document.getElementById('max-price').value.trim() : '';
      if(min) params.set('min_price', min);
      if(max) params.set('max_price', max);
      const sort = document.getElementById('sort-select') ? document.getElementById('sort-select').value : '';
      if(sort) params.set('sort', sort);
      const url = productlistUrl;
      const query = params.toString();
      window.location.href = query ? (url + '?' + query) : url;
    }

    document.querySelectorAll('input[name="category"]').forEach(ch => ch.addEventListener('change', submitFilters));
    ['min-price','max-price'].forEach(id => { const el = document.getElementById(id); if(el) el.addEventListener('change', submitFilters); });
    const sortEl = document.getElementById('sort-select'); if(sortEl) sortEl.addEventListener('change', submitFilters);
    const clearBtn = document.getElementById('clear-filters'); if(clearBtn) clearBtn.addEventListener('click', function(e){ e.preventDefault(); window.location.href = productlistUrl; });
  }

  function initSelectedCategory(){
    const sel = document.getElementById('selectedCategory');
    if(sel && sel.value){
      const btn = document.querySelector("button[data-cat='"+sel.value+"']");
      if(btn) btn.classList.add('border-primary');
    }
  }

  function initDropzone(){
    const fileInput = document.getElementById('dropzone-file');
    const filenameEl = document.getElementById('dropzone-filename');
    if(!fileInput || !filenameEl) return;
    fileInput.addEventListener('change', function(){ const file = this.files[0]; filenameEl.textContent = file ? file.name : ''; });
  }

  function initFileTriggers(){
    document.querySelectorAll('[data-trigger-file]').forEach(btn => {
      btn.addEventListener('click', function(){ const id = this.dataset.triggerFile; const inp = document.getElementById(id); if(inp) inp.click(); });
    });
  }

  document.addEventListener("DOMContentLoaded", function(){
  var sel = document.getElementById('selectedCategory');
  if(sel){
    var val = sel.value;
    if(val){
      var btn = document.querySelector("button[data-cat='"+val+"']");
      if(btn) btn.classList.add('border-primary');
    }
  }
});

  // Initialize on DOM ready and expose helper
  document.addEventListener('DOMContentLoaded', function(){
    window.setSelectedCategory = setSelectedCategory;
    initSelectedCategory();
    initSearchSuggestions();
    initHorizontalScroll();
    initProductFilters();
    initDropzone();
    initFileTriggers();
  });
})();
