

class Controller {
    constructor (api, table) {
        this.table = table
        this.api = api

        // State control variables
        this.anchor = { x: 0, y: 0 }
        this.shift = false
        this.start = { x: 0, y: 0 }

        // Set websocket events
        this.api.onopen = e => this.onConnect(e)
        this.api.onmessage = e => this.onMessage(e)
        this.api.onclose = e => this.onClose(e)

        // Set mouse events
        this.table.table.onclick = e => this.onClick(e)
        this.table.table.onmousedown = e => this.onMouseDown(e)
        this.table.table.onmouseup = e => this.onMouseUp(e)
        window.onwheel = e => this.onWheel(e)

        // Set keyboard events
        window.onkeydown = e => this.onKeyDown(e)
        window.onkeyup = e => this.onKeyUp(e)
        window.onkeypress = e => this.onKeyPress(e)
    }

    onMouseDown (e) {
        // Ignore other buttons
        if (e.buttons != 1)
            return

        this.start = { x: e.clientX, y: e.clientY }
    }

    onMouseUp (e) {
        const { x, y } = this.start

        const moveX = Math.floor((e.clientX - x) / 13)
        const moveY = Math.floor((e.clientY - y) / 15)

        this.move(-moveX, -moveY)
    }

    onWheel (e) {
        const movement = Math.sign(e.deltaY) * 10

        // Horizontal
        if (this.shift)
            return this.move(movement, 0)
        // Vertical
        else
            return this.move(0, movement)
    }

    onClick (e) {
        if (e.target.id == 'table')
            return

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
                this.shift = !this.shift
                return
            // CTRL
            case 17:
                return
            // Caps Lock
            case 20:
                return
            // Left
            case 37:
                return this.table.select(x - 1, y)
            // Up
            case 38:
                return this.table.select(x, y - 1)
            // Right
            case 39:
                return this.table.select(x + 1, y)
            // Down
            case 40:
                return this.table.select(x, y + 1)
            // Delete
            case 46:
                this.set(x + 1, y, ' ')
                return this.table.select(x + 1, y)
        }
    }

    onKeyUp (e) {
        switch (e.keyCode) {
            // Shift
            case 16:
                this.shift = !this.shift
                return
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
        this.table.move(x, y)

        this.anchor.x += x
        this.anchor.y += y

        if (x < 0)
            this._move_right(-x)
        if (x > 0)
            this._move_left(x)
        if (y < 0)
            this._move_up(-y)
        if (y > 0)
            this._move_down(y)

        return this.anchor
    }

    _move_right (moveX) {
        const { x, y } = this.anchor
        const rows = this.table.rows
        this.api.area(x, y, moveX, rows)
    }

    _move_left (moveX) {
        const { x, y } = this.anchor
        const { cols, rows } = this.table
        console.log(x, y, moveX, rows)
        this.api.area(x - moveX + cols, y, moveX, rows)
    }

    _move_up (moveY) {
        const { x, y } = this.anchor
        const cols = this.table.cols
        this.api.area(x, y, cols, moveY)
    }

    _move_down (moveY) {
        const { x, y } = this.anchor
        const { cols, rows } = this.table
        this.api.area(x, y - moveY + rows, cols, moveY)
    }

    set (x, y, c) {
        this.api.set(x + this.anchor.x, y + this.anchor.y, c)
        this.table.set(x, y, c)
    }
}
