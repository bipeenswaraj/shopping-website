import asyncio
from pyppeteer import launch

async def main():
    browser = await launch()
    page = await browser.newPage()

    await page.goto('events.html')

    wrapper = await page.querySelector(".sliderWrapper")
    menuItems = await page.querySelectorAll(".menuItem")
    currentProductImg = await page.querySelector(".productImg")
    currentProductTitle = await page.querySelector(".productTitle")
    currentProductPrice = await page.querySelector(".productPrice")
    currentProductColors = await page.querySelectorAll(".color")
    currentProductSizes = await page.querySelectorAll(".size")
    productButton = await page.querySelector(".productButton")
    payment = await page.querySelector(".payment")
    close = await page.querySelector(".close")

    products = [
        {
            'id': 1,
            'title': "Air Force",
            'price': 119,
            'colors': [
                {'code': "black", 'img': "./img/air.png"},
                {'code': "darkblue", 'img': "./img/air2.png"},
            ],
        },
        {
            'id': 2,
            'title': "Air Jordan",
            'price': 149,
            'colors': [
                {'code': "lightgray", 'img': "./img/jordan.png"},
                {'code': "green", 'img': "./img/jordan2.png"},
            ],
        },
        {
            'id': 3,
            'title': "Blazer",
            'price': 109,
            'colors': [
                {'code': "lightgray", 'img': "./img/blazer.png"},
                {'code': "green", 'img': "./img/blazer2.png"},
            ],
        },
        {
            'id': 4,
            'title': "Crater",
            'price': 129,
            'colors': [
                {'code': "black", 'img': "./img/crater.png"},
            ],
        },
        {
            'id': 5,
            'title': "Hippie",
            'price': 99,
            'colors': [
                {'code': "gray", 'img': "./img/hippie.png"},
                {'code': "black", 'img': "./img/hippie2.png"},
            ],
        },
    ]

    choosenProduct = products[0]

    async def change_slide(index):
        await wrapper.evaluate('(index) => { this.style.transform = `translateX(${-100 * index}vw)`; }')

    async def change_product_texts():
        await currentProductTitle.evaluate('(text) => { this.textContent = text; }', choosenProduct['title'])
        await currentProductPrice.evaluate('(price) => { this.textContent = "$" + price; }', choosenProduct['price'])
        await currentProductImg.evaluate('(img) => { this.src = img; }', choosenProduct['colors'][0]['img'])

    async def assign_colors():
        for index, color in enumerate(currentProductColors):
            await color.evaluate('(code) => { this.style.backgroundColor = code; }', choosenProduct['colors'][index]['code'])

    async def change_product_color(index):
        await currentProductImg.evaluate('(img) => { this.src = img; }', choosenProduct['colors'][index]['img'])

    async def change_product_size(index):
        for size in currentProductSizes:
            await size.evaluate('() => { this.style.backgroundColor = "white"; this.style.color = "black"; }')
        await currentProductSizes[index].evaluate('() => { this.style.backgroundColor = "black"; this.style.color = "white"; }')

    async def product_button_click():
        await payment.evaluate('() => { this.style.display = "flex"; }')

    async def close_click():
        await payment.evaluate('() => { this.style.display = "none"; }')

    async def attach_event_listeners():
        async def menu_item_click(index):
            await change_slide(index)
            nonlocal choosenProduct
            choosenProduct = products[index]
            await change_product_texts()
            await assign_colors()

        async def color_click(index):
            await change_product_color(index)

        async def size_click(index):
            await change_product_size(index)

        await page.evaluate('''(menuItems) => {
            menuItems.forEach((item, index) => {
                item.addEventListener("click", () => menu_item_click(index));
            });
        }''', menuItems)

        await page.evaluate('''(currentProductColors) => {
            currentProductColors.forEach((color, index) => {
                color.addEventListener("click", () => color_click(index));
            });
        }''', currentProductColors)

        await page.evaluate('''(currentProductSizes) => {
            currentProductSizes.forEach((size, index) => {
                size.addEventListener("click", () => size_click(index));
            });
        }''', currentProductSizes)

        await productButton.evaluate('''() => {
            this.addEventListener("click", () => product_button_click());
        }''')

        await close.evaluate('''() => {
            this.addEventListener("click", () => close_click());
        }''')

    await attach_event_listeners()

    # Do other stuff here if needed

    # Close the browser
    await browser.close()

asyncio.get_event_loop().run_until_complete(main())
