<a id="readme-top"></a>

<!-- ABOUT THE PROJECT -->
## About The Project

This project aims to make an extensible program for converting IFC files into RDF graphs with Brick schema. The current implementation is able to map elements from an IFC file to its quantitative properties and can map various relationships between elements. However, it is currently limited in the number of relationships it can recognize and the specificity it can reach when assigning brick classes to nodes. 

Challenges in implementing this project stemmed largely from two areas. First, there is no common data standard for IFC files. Many aspects of these files vary from business to business to include, but not limited to, the IFC class used for an entity (e.g. both IfcWall and IfcStandardWall exist), the relationship used to connect two entities, and the naming scheme used to store various properties. Parsing entities and relationships programmatically relied on the assumption that certain classes as a standard superclass for certain concepts. For example, it is assumed that all relationships are stored under an 'IfcRelationship' and all entities are either an 'IfcSpatialStructureElement' or an 'IfcPhysicalElement'. It is possible that some aspects may be missed with this approach, but it guarantees that no incorrect aspects are grabbed as long as the IFC file is implemented properly. Non-quantitative properties are currently not supported in order to avoid too many extraneous properties. Some files also have non-unique property names, making it difficult to pull the "right" property in all cases.

The other main challenge faced was that there is no clear one-to-one mapping between IFC classes and brick classes. Certain mappings, like what constitutes a 'hasPart' or 'feeds' relationship, were seen as necessary and had to be manually defined. If a mapping wasn't manually defined, IFC classes were matched conservatively to brick classes with the assumption that an IFC class mapped to a brick class if and only if their names (after cleaning) matched exactly. Otherwise, there was a risk of incorrectly mapping in detrimental ways. For example, loosely searching for matches or using a Levenshtein distance metric would map an 'IfcBuildingStorey' to a 'brick:Building' rather than a 'brick:Level'.

The current implementation assumes all classes and properties stored in the final rdf graph come from the brick ontology. Future implementations should add handling for more specific namespaces.

There is currently no direct support for importing the generated rdf graph to neo4j. However, build files are included for starting a neo4j database through docker.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these steps.

### Prerequisites

The following are necessary to run this project:
* python
* neo4j
* docker

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/katelanman/syyclops-assignment.git
   ```
3. Install required python packages
   ```sh
   pip install ifcopenshell pandas rdflib requests beautifulsoup4 os
   ```

5. Change git remote url to avoid accidental pushes to base project
   ```sh
   git remote set-url origin github_username/repo_name
   git remote -v # confirm the changes
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

```sh
python code/load_ifc.py --ifc_file path/to/your.ifc --namespace your_namespace --write_path path/to/output.ttl
```

_For more examples, please refer to the [Documentation](https://example.com)_

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/github_username/repo_name.svg?style=for-the-badge
[contributors-url]: https://github.com/github_username/repo_name/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/github_username/repo_name.svg?style=for-the-badge
[forks-url]: https://github.com/github_username/repo_name/network/members
[stars-shield]: https://img.shields.io/github/stars/github_username/repo_name.svg?style=for-the-badge
[stars-url]: https://github.com/github_username/repo_name/stargazers
[issues-shield]: https://img.shields.io/github/issues/github_username/repo_name.svg?style=for-the-badge
[issues-url]: https://github.com/github_username/repo_name/issues
[license-shield]: https://img.shields.io/github/license/github_username/repo_name.svg?style=for-the-badge
[license-url]: https://github.com/github_username/repo_name/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/linkedin_username
[product-screenshot]: images/screenshot.png
[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[Angular-url]: https://angular.io/
[Svelte.dev]: https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00
[Svelte-url]: https://svelte.dev/
[Laravel.com]: https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white
[Laravel-url]: https://laravel.com
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com 
