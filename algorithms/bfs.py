from collections import deque
from game.base_player import Player
from game.flow_free import FlowFreeBoard, Connection

class BFSPlayer(Player):
    def __init__(self, show_steps: bool = False):
        super().__init__()
        self._planned = False
        self._plan = deque()
        self._done = False
        self._show_steps = show_steps

    class _State:
        def __init__(self, matrix, endpoints, parent=None, op=None, depth=0):
            self.m = tuple(tuple(row) for row in matrix)
            self._rows = len(matrix)
            self._cols = len(matrix[0]) if matrix else 0
            self._endpoints = endpoints
            self.parent = parent
            self.op = op
            self.depth = depth

        def __hash__(self): return hash(self.m)
        def __eq__(self, o): return isinstance(o, BFSPlayer._State) and self.m == o.m

        def _in(self, x, y): return 0 <= x < self._cols and 0 <= y < self._rows
        def _cell(self, x, y): return self.m[y][x]

        def _paint(self, color, to_xy):
            x, y = to_xy
            new = [list(r) for r in self.m]
            new[y][x] = color.lower()
            return new

        def _frontiers_for(self, color):
            p1, p2 = self._endpoints[color]
            low = color.lower()
            cells = {(x, y) for y in range(self._rows) for x in range(self._cols) if self._cell(x, y) == low}
            if not cells:
                return [p1, p2]
            def same(x, y):
                c = self._cell(x, y)
                return c == low or (x, y) == p1 or (x, y) == p2
            fronts = []
            for (x, y) in cells:
                deg = 0
                for dx, dy in ((0,-1),(0,1),(-1,0),(1,0)):
                    nx, ny = x+dx, y+dy
                    if self._in(nx, ny) and same(nx, ny):
                        deg += 1
                if deg != 2:
                    fronts.append((x, y))
            for ep in (p1, p2):
                x, y = ep
                k = 0
                for dx, dy in ((0,-1),(0,1),(-1,0),(1,0)):
                    nx, ny = x+dx, y+dy
                    if self._in(nx, ny) and self._cell(nx, ny) == low:
                        k += 1
                if k <= 1:
                    fronts.append(ep)
            seen, uniq = set(), []
            for p in fronts:
                if p not in seen:
                    uniq.append(p); seen.add(p)
            return uniq

        def goal_test(self):
            for row in self.m:
                for v in row:
                    if v == '.':
                        return False
            from collections import deque
            for color, (p1, p2) in self._endpoints.items():
                Q, seen = deque([p1]), {p1}
                def ok(x,y):
                    v = self._cell(x,y)
                    return v == color.lower() or (isinstance(v, str) and v.isupper() and v.upper()==color.upper())
                found = False
                while Q:
                    x,y = Q.popleft()
                    if (x,y)==p2: found = True; break
                    for dx,dy in ((0,-1),(0,1),(-1,0),(1,0)):
                        nx,ny = x+dx,y+dy
                        if 0<=nx<self._cols and 0<=ny<self._rows and (nx,ny) not in seen and ok(nx,ny):
                            seen.add((nx,ny)); Q.append((nx,ny))
                if not found: return False
            return True

        def neighbors(self):
            nbrs = []
            for color in self._endpoints.keys():
                for fx, fy in self._frontiers_for(color):
                    for dx, dy in ((0,-1),(0,1),(-1,0),(1,0)):
                        nx, ny = fx+dx, fy+dy
                        if not self._in(nx, ny): continue
                        t = self._cell(nx, ny)
                        if t == '#': continue
                        if isinstance(t, str) and t.isupper() and t.upper()!=color.upper():
                            continue
                        if isinstance(t, str) and t.islower() and t != color.lower():
                            continue
                        if t == color.lower():
                            continue
                        if t == '.':
                            new_m = self._paint(color, (nx, ny))
                            op = (color, (fx, fy), (nx, ny))
                            nbrs.append(BFSPlayer._State(new_m, self._endpoints, parent=self, op=op, depth=self.depth+1))
                        elif isinstance(t, str) and t.isupper() and t.upper()==color.upper():
                            op = (color, (fx, fy), (nx, ny))
                            nbrs.append(BFSPlayer._State([list(r) for r in self.m], self._endpoints, parent=self, op=op, depth=self.depth+1))
            return nbrs

    def _plan_with_bfs(self, board: FlowFreeBoard):
        mat = board.get_state()
        endpoints = {}
        for y, row in enumerate(mat):
            for x, v in enumerate(row):
                if isinstance(v, str) and v.isupper() and v not in ('.', '#'):
                    endpoints.setdefault(v.lower(), []).append((x, y))
        endpoints = {c: (pts[0], pts[1]) for c, pts in endpoints.items() if len(pts)==2}

        start = BFSPlayer._State(mat, endpoints)
        frontier = deque([start])
        explored = set()
        max_depth = 0
        solution = None

        while frontier:
            st = frontier.popleft()
            if st in explored:
                continue
            explored.add(st)
            if st.goal_test():
                solution = st
                break
            for nb in st.neighbors():
                if nb not in explored:
                    frontier.append(nb)
                    if nb.depth > max_depth:
                        max_depth = nb.depth

        if not solution:
            return []

        ops = []
        cur = solution
        while cur.parent is not None:
            ops.append(cur.op)
            cur = cur.parent
        ops.reverse()
        return ops

    def play(self, board: FlowFreeBoard):
        if self._done:
            return None

        if not self._planned:
            self._plan = deque(self._plan_with_bfs(board))
            for conn in board.connections:
                conn.clean_road()
            self._planned = True

        if not self._plan:
            self._done = True
            return None

        color, _frm, to_xy = self._plan.popleft()
        cmap = {c.name: c for c in board.connections}
        conn = cmap[color]
        conn.add_to_road(to_xy)
        if self._show_steps:
            board.show()
        return to_xy
