# Modulo per mettere Javascript e HTML

import time
import IPython
from random import choice
import json
from IPython.display import display, HTML, IFrame, Javascript

html = IPython.display.HTML('''
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">

    <title>Tree Example</title>

    <style>

	.node {
		cursor: pointer;
	}

	.node circle {
	  fill: #fff;
	  stroke: steelblue;
	  stroke-width: 3px;
	}

	.node text {
	  font: 14px sans-serif;
	}

	.link {
	  fill: none;
	  stroke: #ccc;
	  stroke-width: 2px;
	}

    </style>

  </head>

  <body>
    <!-- load the d3.js library -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/d3/3.5.17/d3.min.js"></script>
  </body>
</html>
''')

js = IPython.display.Javascript('''
// ************** Generate the tree diagram	 *****************
var margin = {top: 20, right: 120, bottom: 20, left: 120},
	width = 1920 - margin.right - margin.left,
	height = 800 - margin.top - margin.bottom;

var i = 0,
  // NOTE(suo): Disable animation for now
	// duration = 300,
  duration = 0,
	root;

var tree = d3.layout.tree() // Qui ho caricato la libreria d3: per farlo ho dovuto 'entrare' in Javascript
	.size([height, width]);

var diagonal = d3.svg.diagonal()
	.projection(function(d) { return [d.y, d.x]; });

var svg = d3.select("body").append("svg")
	.attr("width", width + margin.right + margin.left)
	.attr("height", height + margin.top + margin.bottom)
  .append("g")
	.attr("transform", "translate(" + margin.left + "," + margin.top + ")");

d3.select(self.frameElement).style("height", "500px");

function update(source) {

  // Compute the new tree layout.
  var nodes = tree.nodes(root).reverse(),
	  links = tree.links(nodes);

  // Normalize for fixed-depth.
  nodes.forEach(function(d) { d.y = d.depth * 180; });

  // Update the nodes…
  var node = svg.selectAll("g.node")
	  .data(nodes, function(d) { return d.id || (d.id = ++i); });

  // Enter any new nodes at the parent's previous position.
  var nodeEnter = node.enter().append("g")
	  .attr("class", "node")
	  .attr("transform", function(d) { return "translate(" + source.y0 + "," + source.x0 + ")"; })
	  .on("click", click);

  nodeEnter.append("circle")
	  .attr("r", 1e-6)
	  .style("fill", function(d) {
      if (d._children)
        return "lightsteelblue";
      else {
        if (d.selected) {
          return "red";
        } else {
          return "#fff";
        }
      }
    });

  // NOTE(suo): Disable node name
  // nodeEnter.append("text")
	//   .attr("x", function(d) { return d.children || d._children ? -13 : 13; })
	//   .attr("dy", ".35em")
	//   .attr("text-anchor", function(d) { return d.children || d._children ? "end" : "start"; })
	//   .text(function(d) { return d.name; })
	//   .style("fill-opacity", 1e-6);

  nodeEnter.append("text")
	  .attr("x", function(d) { return d.children || d._children ? -13 : 13; })
	  .attr("dy", "-0.65em")
	  .attr("text-anchor", function(d) { return d.children || d._children ? "end" : "start"; })
	  .text(function(d) { return 'Value: ' + d3.format(".2f")(d.value); })
	  .style("fill-opacity", 1e-6);

  nodeEnter.append("text")
	  .attr("x", function(d) { return d.children || d._children ? -13 : 13; })
	  .attr("dy", "0.35em")
	  .attr("text-anchor", function(d) { return d.children || d._children ? "end" : "start"; })
	  .text(function(d) { return 'Prior: ' + d3.format(".2f")(d.prior); })
	  .style("fill-opacity", 1e-6);

  nodeEnter.append("text")
	  .attr("x", function(d) { return d.children || d._children ? -13 : 13; })
	  .attr("dy", "1.35em")
	  .attr("text-anchor", function(d) { return d.children || d._children ? "end" : "start"; })
	  .text(function(d) { return 'Visit Count: \t' + d.visit_count; })
	  .style("fill-opacity", 1e-6);

  // Transition nodes to their new position.
  var nodeUpdate = node.transition()
	  .duration(duration)
	  .attr("transform", function(d) { return "translate(" + d.y + "," + d.x + ")"; });

  nodeUpdate.select("circle")
	  .attr("r", 10)
	  .style("fill", function(d) {
      if (d._children)
        return "lightsteelblue";
      else {
        if (d.selected) {
          return "red";
        } else {
          return "#fff";
        }
      }
     });

  nodeUpdate.selectAll("text")
	  .style("fill-opacity", 1);

  // Transition exiting nodes to the parent's new position.
  var nodeExit = node.exit().transition()
	  .duration(duration)
	  .attr("transform", function(d) { return "translate(" + source.y + "," + source.x + ")"; })
	  .remove();

  nodeExit.select("circle")
	  .attr("r", 1e-6);

  nodeExit.selectAll("text")
	  .style("fill-opacity", 1e-6);

  // Update the links…
  var link = svg.selectAll("path.link")
	  .data(links, function(d) { return d.target.id; });

  // Enter any new links at the parent's previous position.
  link.enter().insert("path", "g")
	  .attr("class", "link")
	  .attr("d", function(d) {
		var o = {x: source.x0, y: source.y0};
		return diagonal({source: o, target: o});
	  });

  // Transition links to their new position.
  link.transition()
	  .duration(duration)
	  .attr("d", diagonal);

  // Transition exiting nodes to the parent's new position.
  link.exit().transition()
	  .duration(duration)
	  .attr("d", function(d) {
		var o = {x: source.x, y: source.y};
		return diagonal({source: o, target: o});
	  })
	  .remove();

  // Stash the old positions for transition.
  nodes.forEach(function(d) {
	d.x0 = d.x;
	d.y0 = d.y;
  });
}

// Toggle children on click.
function click(d) {
  if (d.children) {
	d._children = d.children;
	d.children = null;
  } else {
	d.children = d._children;
	d._children = null;
  }
  update(d);
}
''')

update_js_str = '''

function merge(a, b) {
  a.value = b.value;
  if (!b.children) {
    a.children = b.children;
  }
  else {
    if (!a.children) {
      a.children = [];
    }

    for (i=0;i<b.children.length;i++) {
      if (i < a.children.length) {
        merge(a.children[i], b.children[i])
      } else {
        a.children.push(b.children[i])
      }
    }
  }
}

treeDataLoaded = [%s];

if (window.treeData) {
  // merge(window.treeData[0], treeDataLoaded[0])
  window.treeData = treeDataLoaded;
} else {
  window.treeData = treeDataLoaded;
}

// ************** Generate the tree diagram	 *****************
var margin = {top: 20, right: 120, bottom: 20, left: 120},
	width = 1920 - margin.right - margin.left,
	height = 800 - margin.top - margin.bottom;

root = window.treeData[0];
root.x0 = height / 2;
root.y0 = 0;

update(root);
'''