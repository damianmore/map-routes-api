from utils import *
from path_finding import *
import folium  # I think we should use Plotly due to its ability to update live...


class MapAPI:
    def __init__(self, view_location: str | tuple[float, float]):
        self._viewLocation = normalize_location_input(view_location)
        self._map = None
        self.graph = None

    def update_view_location(self, new_location: str | tuple[float, float]):
        self._viewLocation = normalize_location_input(new_location)

    def create_map(self):
        self._map = folium.Map(location=self._viewLocation)

    def draw_maker(self, location: str | tuple[float, float], on_hover_text: str, popup_text: str, icon: str):
        folium.Marker(
            location=[*location],
            tooltip=on_hover_text,
            popup=popup_text,
            icon=folium.Icon(icon=icon),
        ).add_to(self._map)

    def draw_shortest_path(self, start: str | tuple[float, float], end: str | tuple[float, float], network_type: str):
        start = normalize_location_input(start)
        end = normalize_location_input(end)

        graph = get_graph(start, end, network_type)
        start_node = find_nearest_node(start)
        end_node = find_nearest_node(end)

        route_nodes = shortest_path(graph, start_node, end_node)
        route_coords = [(graph.nodes[node]["y"], graph.nodes[node]["x"]) for node in route_nodes]

        folium.PolyLine(route_coords, color="blue", weight=5, opacity=0.8).add_to(self._map)

    def download_map(self, filename: str):
        self._map.save(filename)