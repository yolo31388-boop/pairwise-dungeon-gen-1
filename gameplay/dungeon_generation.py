import math

def room_overlap(a, b):
    """房间包围盒相交。包围盒为 (x, y, w, h)，做完整 AABB 相交而非仅中心距。"""
    ax, ay, aw, ah = a
    bx, by, bw, bh = b
    return ax < bx + bw and bx < ax + aw and ay < by + bh and by < ay + ah

def corridor_cells(a, b):
    """走廊格数。两点间 L 形走廊覆盖的格子数（含两端）。"""
    (x1, y1), (x2, y2) = a, b
    return abs(x2 - x1) + abs(y2 - y1) + 1

def rng_seed(base, room_id):
    """房间独立种子。每个房间派生自己的 RNG 种子，避免并行生成共享全局状态。"""
    return base * 100 + room_id

def connectivity(parents):
    """连通分量。parents[i] 为节点 i 的父节点，0 为空指针哨兵（根），统计根节点数量。"""
    return sum(1 for p in parents if p == 0)

def key_before_door(key_room, door_room):
    """钥匙门拓扑。钥匙所在房间必须在门之前可达（拓扑序更小）。"""
    return key_room < door_room

def depth_difficulty(depth, base):
    """可达深度难度。按从入口的可达深度而非房间序号分配难度。"""
    return base + depth

def navmesh_door_cells(width, height):
    """门洞 navmesh。门洞区域需要同步挖开的导航格数。"""
    return width * height

def stair_pair(floor_a, floor_b):
    """楼梯双向。返回规范化（低层, 高层）的双向连接对。"""
    return (min(floor_a, floor_b), max(floor_a, floor_b))

def generation_done(progress):
    """生成完成。进度达到 1.0 才允许放入玩家，避免脚下 tile 被改写。"""
    return progress >= 1.0

def layout_digest(seed, rooms):
    """布局摘要。存档保存种子与布局摘要，版本更新后可校验一致性。"""
    return f"{seed}:{rooms}"

def dead_end_keep(dead_end, critical):
    """死路保护。关键路径上的房间不可清理；普通死路保留。"""
    return dead_end or critical

def room_bounds(center, size, rotation):
    """旋转房包围盒。返回旋转后归一化的 (长, 宽) 尺寸。"""
    w, h = size
    if rotation % 180 != 0:
        w, h = h, w
    return (max(w, h), min(w, h))

def grid_index(x, y, width):
    """网格索引。行优先展开为一维索引。"""
    return y * width + x

def step_limit(distance, step):
    """步数上限。覆盖 distance 所需的步数（向上取整）。"""
    return math.ceil(distance / step)

def seed_key(seed, version):
    """存档种子键。种子与生成版本绑定，避免版本更新后同 seed 布局漂移。"""
    return f"{seed}:{version}"
