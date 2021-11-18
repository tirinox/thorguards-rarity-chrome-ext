function update() {
    const selectors = [
        'div.AssetCardFooter--name',
        'h1.item--title',
        'div.kohuDY'
    ]

    for(const selector of selectors) {
        const items = document.querySelectorAll(selector);
        for(const item of items) {
            try {
                addRarity(item)
            } catch {}
        }
    }
}

setInterval(update, 2000)


function addRarity(el) {
    const text = el.innerText
    if(!text.startsWith('[R:') && text.startsWith('ThorGuards #')) {
        const split = text.split('#')
        if(split.length >= 1) {
            const ident = parseInt(split[1])
            const r = RANKS[ident]
            el.innerText = `[R:${r}] ${text}`
        }
    }
}

