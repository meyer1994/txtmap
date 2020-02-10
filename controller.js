

class Controller {
    constructor () {
        const cols = Math.floor(window.innerWidth / 13)
        const rows = Math.floor(window.innerHeight / 15)

        const el = document.getElementById('table')
        this.table = new Table(cols, rows, el)
        this.api = new API()

        this.anchor = { x: 0, y: 0 }

        // Set WS events
        this.api.onopen = e => this.onConnect(e)
        this.api.onmessage = e => this.onMessage(e)
        this.api.onclose = e => this.onClose(e)

        // Set viewport events
        this.table.table.onclick = e => this.onClick(e)
        window.onkeydown = e => this.onKeyDown(e)
        window.onwheel = e => this.onWheel(e)
    }

    onWheel (e) {
        const horizontal = Math.sign(e.deltaX) * 10
        const vertical = Math.sign(e.deltaY) * 10

        this.move(horizontal, vertical)

        const { x, y } = this.anchor
        this.api.area(x, y, this.table.cols, this.table.rows)
    }

    onClick (e) {
        const td = e.target
        const tr = td.parentElement

        const x = Number.parseInt(td.id)
        const y = Number.parseInt(tr.id)

        this.table.select(x, y)
    }

    onKeyPress (e) {
        const { x, y } = this.table.coord
        this.set(x, y, e.key)
        return this.table.select(x + 1, y)
    }

    onKeyDown (e) {
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
            // Up
            case 38:
                return this.table.select(x, y - 1)
            // Down
            case 40:
                return this.table.select(x, y + 1)
            // Right
            case 39:
                return this.table.select(x + 1, y)
            // Left
            case 37:
                return this.table.select(x - 1, y)
        }
    }

    onConnect (e) {
        console.debug('Connected')
        const cols = this.table.cols
        const rows = this.table.rows
        this.api.area(0, 0, cols, rows)
    }

    onMessage (e) {
        console.debug(`Message: ${e.data.length} bytes`)
        let data = JSON.parse(e.data)

        const aX = this.anchor.x
        const aY = this.anchor.y

        for (const [x, y, char] of data)
            this.table.set(x - aX, y - aY, char)
    }

    onClose (e) {
        console.debug('Closed')
    }

    move (x, y) {
        this.anchor.x += x
        this.anchor.y += y
    }

    set (x, y, c) {
        this.api.set(x + this.anchor.x, y + this.anchor.y, c)
        this.table.set(x, y, c)
    }
}
