
class Table {
    constructor (cols, rows, element) {
        this.cols = cols
        this.rows = rows
        this.coord = { x: 0, y: 0 }
        this.table = element

        console.debug(`Table: ${this.cols} cols, ${this.rows} rows`)

        // Rows
        for (let i = 0; i < rows; i++) {
            const tr = document.createElement('tr')
            tr.id = i
            element.appendChild(tr)

            // Cols
            for (let j = 0; j < cols; j++) {
                const td = document.createElement('td')
                td.id = j
                tr.appendChild(td)
            }
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
