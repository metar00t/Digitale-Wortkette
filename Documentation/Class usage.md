# Execute Example:
In the example from execute File it was found out that the following doesnt work:

```python
import Controller.SwaggerController

import Controller
import Controller.SwaggerController
```
All of those examples do not work because we use the folder structure for 
navigating and importing the files and this doesnt work since we need the class also or in this case the modules.

___________________________

The following examples of imports do work:
```python
from Controller import SwaggerController 
api.add_resource(SwaggerController.SwaggerController,"/temp")
_________________

from Controller.SwaggerController import SwaggerController
api.add_resource(SwaggerController,"/temp")
```

Those Examples do work because the import goes to the Controller folder and the imports the file SwaggerController and in the 2. example the SwaggerController Module.