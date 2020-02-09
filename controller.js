

class Controller {
    constructor () {
        const cols = window.innerWidth / 13
        const rows = window.innerHeight / 15

        const el = document.getElementById('table')
        this.table = new Table(cols, rows, el)
        this.api = new API()

        this.api.onopen = e => this.onConnect(e)
        this.api.onmessage = e => this.onMessage(e)
    }

    addClickListenerToTableCells () {
        for (let i = 0; i < this.table.rows; i++) {
            for (let j = 0; j < this.table.cols; j++) {
                const cell = this.table.get(j, i)
                cell.addEventListener('click', e => {
                    const td = e.target
                    const tr = td.parentElement
                    this.table.select(td.id, tr.id)
                })
            }
        }
    }

    addKeyPressListenerToWindow () {
        window.onkeydown = e => {
            const { x, y } = this.table.coord

            switch (e.keyCode) {
                // Tab
                case 9:
                    return e.preventDefault()
                // Backspace
                case 8:
                    this.set(x - 1, y, ' ')
                    return this.table.select(x - 1, y)
                // Enter
                case 13:
                    return this.table.select(x, y + 1)
                // Shift
                case 16:
                    return
                // CTRL
                case 17:
                    return
                // Caps Lock
                case 20:
                    return
                default:
                    this.set(x, y, e.key.charAt(0))
                    return this.table.select(x + 1, y)
            }
        }
    }

    onConnect (e) {
        const cols = this.table.cols
        const rows = this.table.rows

        this.api.area(0, 0, cols, rows)
    }

    onMessage (e) {
        let data = JSON.parse(e.data)

        if (!Array.isArray(data))
            data = [data]

        for (const [x, y, char] of data) {
            this.table.set(x, y, char)
        }
    }

    set (x, y, c) {
        if (c !== ' ')
            this.api.set(x, y, c)
        this.table.set(x, y, c)
    }
}
