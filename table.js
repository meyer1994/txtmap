
class Table {
    constructor (cols, rows, element) {
        this.cols = cols
        this.rows = rows
        this.coord = { x: 0, y: 0 }
        this.table = element

        console.debug(`Table: ${this.cols} cols, ${this.rows} rows`)
        this._init()
    }

    _init () {
        // Rows
        for (let i = 0; i < this.rows; i++) {
            const tr = document.createElement('tr')
            tr.id = i
            this.table.appendChild(tr)

            // Cols
            for (let j = 0; j < this.cols; j++) {
                const td = document.createElement('td')
                td.id = j
                tr.appendChild(td)
            }
        }
    }

    move (x, y) {
        if (x < 0)
            this._move_right(-x)
        if (x > 0)
            this._move_left(x)
        if (y < 0)
            this._move_up(-y)
        if (y > 0)
            this._move_down(y)

        for (let i = 0; i < this.rows; i++) {
            const tr = this.table.children[i]
            tr.id = i
            for (let j = 0; j < this.cols; j++) {
                const td = tr.children[j]
                td.id = j
            }
        }
    }

    _move_right (x) {
        for (const tr of this.table.children) {
            for (let i = 0; i < x; i++) {
                const last = tr.lastChild
                last.innerText = ''
                tr.removeChild(last)
                tr.prepend(last)
            }
        }
    }

    _move_left (x) {
        for (const tr of this.table.children) {
            for (let i = 0; i < x; i++) {
                const first = tr.firstChild
                first.innerText = ''
                tr.removeChild(first)
                tr.appendChild(first)
            }
        }
    }

    _move_up (y) {
        for (let i = 0; i < y; i++) {
            const tr = this.table.lastChild
            for (const td of tr.children) {
                td.innerText = ''
            }
            this.table.removeChild(tr)
            this.table.prepend(tr)
        }
    }

    _move_down (y) {
        for (let i = 0; i < y; i++) {
            const tr = this.table.firstChild
            for (const td of tr.children) {
                td.innerText = ''
            }
            this.table.removeChild(tr)
            this.table.appendChild(tr)
        }
    }

    get (x, y) {
        const tr = this.table.children[y]
        const td = tr.children[x]
        return td
    }

    set (x, y, c) {
        this.get(x, y).innerText = c.charAt(0)
        return this.get(x, y)
    }

    select (x, y) {
        console.debug(`Select: (${x}, ${y})`)

        const current = this.get(this.coord.x, this.coord.y)
        current.classList.remove('selected')

        this.coord = { x: Number.parseInt(x), y: Number.parseInt(y) }

        const cell = this.get(x, y)
        cell.classList.add('selected')
        return cell
    }
}
