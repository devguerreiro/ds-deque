import assert from "assert";

class Node {
    value: number;
    next: Node | null = null;
    previous: Node | null = null;

    constructor(value: number) {
        this.value = value;
    }
}

export class Deque {
    private initial: Node | null = null;
    private size: number = 0;

    private getNode(index: number) {
        const _index = index < 0 ? this.size + index : index;
        let node = this.initial;
        for (let i = 0; i < _index; i++) {
            if (node !== null) {
                node = node.next;
            } else {
                break;
            }
        }
        if (node !== null && !(_index < 0)) {
            return node;
        }
        throw new RangeError();
    }

    append(value: number): void {
        const newNode = new Node(value);
        if (this.size === 0) {
            this.initial = newNode;
        } else {
            let lastNode = this.initial as Node;
            while (lastNode.next !== null) {
                lastNode = lastNode.next;
            }
            lastNode.next = newNode;
            newNode.previous = lastNode;
        }
        this.size++;
    }

    appendLeft(value: number): void {
        const newNode = new Node(value);
        if (this.size === 0) {
            this.initial = newNode;
        } else {
            let firstNode = this.initial as Node;
            while (firstNode.previous !== null) {
                firstNode = firstNode.previous;
            }
            firstNode.previous = newNode;
            newNode.next = firstNode;
            this.initial = newNode;
        }
        this.size++;
    }

    private _extend(values: number[], lastNode: Node) {
        for (let v of values) {
            const newNode = new Node(v);
            lastNode.next = newNode;
            newNode.previous = lastNode;
            lastNode = newNode;
            this.size++;
        }
    }

    extend(values: number[]) {
        if (this.initial === null) {
            this.initial = new Node(values[0]);
            this.size++;
            this._extend(values.slice(1), this.initial);
        } else {
            let lastNode = this.initial;
            while (lastNode.next !== null) {
                lastNode = lastNode.next;
            }
            this._extend(values, lastNode);
        }
    }

    private _extendLeft(values: number[], firstNode: Node) {
        for (let v of values) {
            const newFirst = new Node(v);
            firstNode.previous = newFirst;
            newFirst.next = firstNode;
            firstNode = newFirst;
            this.initial = newFirst;
            this.size++;
        }
    }

    extendLeft(values: number[]) {
        if (this.initial === null) {
            this.initial = new Node(values[0]);
            this.size++;
            this._extend(values.slice(1), this.initial);
        } else {
            this._extend(values, this.initial);
        }
    }

    get(index: number) {
        const node = this.getNode(index);
        return node.value;
    }

    set(index: number, value: number) {
        const node = this.getNode(index);
        node.value = value;
    }

    indexOf(value: number) {
        let node = this.initial;
        let index = 0;
        while (node !== null) {
            if (node.value === value) {
                return index;
            }
            node = node.next;
            index++;
        }
        return -1;
    }

    insert(index: number, value: number) {
        const newNode = new Node(value);
        if (index === 0) {
            newNode.next = this.initial;
            this.initial = newNode;
        } else {
            const previousNode = this.getNode(index - 1);
            newNode.next = previousNode.next;
            previousNode.next = newNode;
        }
        this.size++;
    }

    remove(value: number) {
        if (this.size === 0) {
            throw new Error();
        }
        if (this.initial !== null) {
            if (this.initial.value === value) {
                let aux = this.initial.next;
                this.initial.next = null;
                this.initial = aux;
                this.size--;
                return true;
            } else {
                let previousNode = this.initial;
                let currentNode = previousNode.next;
                while (currentNode !== null) {
                    if (currentNode.value === value) {
                        previousNode.next = currentNode.next;
                        currentNode.next = null;
                        this.size--;
                        return true;
                    }
                    previousNode = currentNode;
                    currentNode = currentNode.next;
                }
                return false;
            }
        }
    }

    get length(): number {
        return this.size;
    }
}

// TODO: convert into unit testing

const deque = new Deque();

const BIG_INDEX = 2 ** 100;

// add to right
deque.append(10);
deque.append(11);
deque.append(12);

// check length
assert.equal(deque.length, 3);

// check get by index
assert.equal(deque.get(0), 10);
assert.equal(deque.get(1), 11);
assert.equal(deque.get(2), 12);

// check inverted get by index
assert.equal(deque.get(-1), 12);
assert.equal(deque.get(-2), 11);
assert.equal(deque.get(-3), 10);

// check index of
assert.equal(deque.indexOf(10), 0);
assert.equal(deque.indexOf(11), 1);
assert.equal(deque.indexOf(12), 2);

// check index of inexistent
assert.equal(deque.indexOf(BIG_INDEX), -1);

// check get by index of an index bigger than length
assert.throws(() => deque.get(BIG_INDEX), RangeError);

// check get by index of an index smaller than negative length
assert.throws(() => deque.get(-BIG_INDEX), RangeError);

// check change index value
deque.set(0, 20);
deque.set(1, 21);
deque.set(2, 22);

assert.equal(deque.get(0), 20);
assert.equal(deque.get(1), 21);
assert.equal(deque.get(2), 22);

// check change inverted index value
deque.set(-1, 32);
deque.set(-2, 31);
deque.set(-3, 30);

assert.equal(deque.get(2), 32);
assert.equal(deque.get(1), 31);
assert.equal(deque.get(0), 30);

// check change index value of an index bigger than length
assert.throws(() => deque.set(BIG_INDEX, 1), RangeError);

// check change index value of an index smaller than negative length
assert.throws(() => deque.set(-BIG_INDEX, 1), RangeError);

const deque2 = new Deque();

// extend to right from empty deque
deque2.extend([1, 2, 3]);

assert.equal(deque2.length, 3);

// check getitem
assert.equal(deque2[0], 1);
assert.equal(deque2[1], 2);
assert.equal(deque2[2], 3);

// extend to right
deque2.extend([13, 14, 15]);

assert.equal(deque2.length, 6);

assert.equal(deque2[3], 15);
assert.equal(deque2[4], 14);
assert.equal(deque2[5], 13);

const deque3 = new Deque();

// extend to left from empty deque
deque3.extendLeft([13, 14, 15]);

assert.equal(deque3.length, 3);

assert.equal(deque3[2], 13);
assert.equal(deque3[1], 14);
assert.equal(deque3[0], 15);

//extend to left
deque3.extendLeft([1, 2, 3]);

assert.equal(deque3.length, 6);

assert.equal(deque3[2], 1);
assert.equal(deque3[1], 2);
assert.equal(deque3[0], 3);

// add to left
deque3.appendLeft(10);
deque3.appendLeft(11);
deque3.appendLeft(12);

assert.equal(deque3.length, 9);

// check getitem
assert.equal(deque3[0], 12);
assert.equal(deque3[1], 11);
assert.equal(deque3[2], 10);

// pop from right
deque3.pop();

assert.equal(deque3.length, 8);

assert.equal(deque3[-1], 14);

// pop from left
deque3.popLeft();

assert.equal(deque3.length, 7);

assert.equal(deque3[0], 11);
