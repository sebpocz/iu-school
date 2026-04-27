#@title \<capture network data>

# we import just the data from season 1
df_edges = pd.read_csv('https://raw.githubusercontent.com/mathbeveridge/gameofthrones/master/data/got-s1-edges.csv')
df_nodes = pd.read_csv('https://raw.githubusercontent.com/mathbeveridge/gameofthrones/master/data/got-s1-nodes.csv')
df_nodes.set_index('Id', inplace=True)

# build graph
G = nx.from_pandas_edgelist(df_edges, 'Source', 'Target', 'Weight')

# calculate communities
communities = community.greedy_modularity_communities(G, weight='Weight')

df_nodes['Community'] = 0
for i, c in enumerate(communities):
    df_nodes.loc[c, 'Community'] = i + 1

df_nodes.loc[:, 'Community'] = df_nodes['Community'].astype(str)

# name a few popular characters according to Google
popular_chars = ['Ned', 'Tyrian', 'Daenerys', 'Arya', 'Jon', 'Eddard', 'Brienne', 'Jaime', 'Cersei', 'Sandor']
df_nodes['Popularity'] = df_nodes['Label'].apply(lambda s: 'Popular' if s in popular_chars else 'Normal')

# calculate networkx layout positions, e.g., `spring_layout`
pos = nx.spring_layout(G)

x = []
y = []

for node in G.nodes():
    x_, y_ = pos[node]
    x.append(x_)
    y.append(y_)

# add locations to node dataset
df_nodes['x'] = x
df_nodes['y'] = y

# calculate max weight for visualizing edges
max_weight = df_edges['Weight'].max()
