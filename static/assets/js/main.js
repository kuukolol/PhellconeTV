AOS.init({ duration: 800, easing: "ease-in-out", once: true });

function handleScroll() {
    const backToTopBtn = document.querySelector('.back-to-top');
    window.onscroll = () => {
        const scrollTop = document.body.scrollTop || document.documentElement.scrollTop;
        backToTopBtn.style.display = scrollTop > 200 ? 'flex' : 'none';
    };
}

function setupMenuHighlighting() {
    const menuItems = document.querySelectorAll('.menu-item');
    menuItems.forEach(item => {
        item.onclick = () => {
            document.querySelector('.menu-item.active')?.classList.remove('active');
            item.classList.add('active');
        };
    });
}

function setupGadgetCategoryFilter() {
    const gadgetMenuList = document.querySelector('.gadget-item-wrap');
    const gadgetCategory = document.querySelector('.gadget-category');

    if (!gadgetMenuList || !gadgetCategory) return;

    const categories = gadgetCategory.querySelectorAll('button');
    categories.forEach(button => {
        button.onclick = e => {
            document.querySelector('.gadget-category button.active')?.classList.remove('active');
            e.target.classList.add('active');
            gadgetMenuList.className = 'gadget-item-wrap ' + e.target.dataset.gadgetType;
        };
    });
}

function isElementInViewport(el) {
    const rect = el.getBoundingClientRect();
    const viewHeight = window.innerHeight || document.documentElement.clientHeight;

    return (
        (rect.top <= 0 && rect.bottom >= 0) ||
        (rect.bottom >= viewHeight && rect.top <= viewHeight) ||
        (rect.top >= 0 && rect.bottom <= viewHeight)
    );
}

function setupScrollAnimations() {
    const elements = document.querySelectorAll('.play-on-scroll');
    const scroll = window.requestAnimationFrame || function (cb) { window.setTimeout(cb, 1000 / 60); };

    function loop() {
        elements.forEach(el => {
            el.classList.toggle('start', isElementInViewport(el));
        });
        scroll(loop);
    }

    loop();
}

function setupBottomNav() {
    const navItems = document.querySelectorAll('.mb-nav-item');
    const moveItem = document.querySelector('.mb-move-item');

    navItems.forEach((item, index) => {
        item.onclick = () => {
            document.querySelector('.mb-nav-item.active')?.classList.remove('active');
            item.classList.add('active');
            moveItem.style.left = `${index * 25}%`;
        };
    });
}

function setupSearchAutocomplete() {
    const searchInput = document.getElementById("gadgetSearch");
    const suggestionBox = document.getElementById("searchSuggestions");

    if (!searchInput || !suggestionBox) return;

    searchInput.addEventListener("input", async () => {
        const query = searchInput.value.trim();
        suggestionBox.innerHTML = "";

        if (!query) return;

        try {
            const res = await fetch(`/search?q=${encodeURIComponent(query)}`);
            const matches = await res.json();

            matches.forEach(gadget => {
                const li = document.createElement("li");
                li.textContent = gadget;
                li.onclick = () => {
                    searchInput.value = gadget;
                    suggestionBox.innerHTML = "";
                };
                suggestionBox.appendChild(li);
            });
        } catch (err) {
            console.error("Error fetching search results:", err);
        }
    });
}

handleScroll();
setupMenuHighlighting();
setupGadgetCategoryFilter();
setupScrollAnimations();
setupBottomNav();
setupSearchAutocomplete();
