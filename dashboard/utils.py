from collections import deque
OCCUPIED_THRESHOLD=15
HIGH_PRESSURE_THRESHOLD=110
MIN_REGION_PIXELS=10

def neighbors(r,c,rows,cols):
    for dr,dc in ((1,0),(-1,0),(0,1),(0,-1)):
        nr,nc=r+dr,c+dc
        if 0<=nr<rows and 0<=nc<cols: yield nr,nc

def connected_regions(matrix, threshold):
    rows=len(matrix); cols=len(matrix[0]) if rows else 0
    visited=[[False]*cols for _ in range(rows)]; regions=[]
    for r in range(rows):
        for c in range(cols):
            if visited[r][c] or matrix[r][c] <= threshold: continue
            q=deque([(r,c)]); visited[r][c]=True; coords=[]; vals=[]
            while q:
                cr,cc=q.popleft(); coords.append((cr,cc)); vals.append(matrix[cr][cc])
                for nr,nc in neighbors(cr,cc,rows,cols):
                    if not visited[nr][nc] and matrix[nr][nc] > threshold:
                        visited[nr][nc]=True; q.append((nr,nc))
            if len(coords) >= MIN_REGION_PIXELS:
                regions.append({'coords':coords,'size':len(coords),'max_value':max(vals),'avg_value':round(sum(vals)/len(vals),2)})
    return regions

def compute_frame_metrics(matrix):
    flat=[v for row in matrix for v in row]
    occupied=sum(1 for v in flat if v>OCCUPIED_THRESHOLD)
    contact=round((occupied/len(flat))*100,2) if flat else 0
    maxp=max(flat) if flat else 0
    avg=round(sum(flat)/len(flat),2) if flat else 0
    high=connected_regions(matrix,HIGH_PRESSURE_THRESHOLD)
    ppi=max([r['max_value'] for r in high], default=maxp)
    flagged=bool(high) or ppi>=HIGH_PRESSURE_THRESHOLD
    return {'peak_pressure_index':round(ppi,2),'contact_area_percent':contact,'occupied_pixels':occupied,'max_pressure':round(maxp,2),'average_pressure':avg,'reposition_per_hour':round(max(0.4, ppi/70),2),'high_pressure_regions':high,'flagged_for_review':flagged,'plain_english_summary':f'Peak pressure {round(ppi,1)} with {contact}% contact area.'}

def heatmap_cells(matrix):
    flat=[v for row in matrix for v in row]; mx=max(flat) if flat else 1; out=[]
    for row in matrix:
      for v in row:
        ratio=v/mx if mx else 0
        if v<20: color,label='#f1f5f9','Low'
        elif v<80: color,label=f'rgba(148,163,184,{min(1,0.35+ratio)})','Medium'
        else: color,label=f'rgba(30,41,59,{min(1,0.35+ratio)})','High'
        out.append({'value':round(v,1),'color':color,'label':label})
    return out
