from workflow.customworkflow.state import State
from workflow.customworkflow.category import Category
from workflow.customworkflow.transition import Transition
from workflow.customworkflow.property import Property, RequireProperty
from workflow.customworkflow.spawnchild import SpawnChild

DEFINITIVE_STATE_SHAPE = 'doubleoctagon'
CONTAINER_STATE_SHAPE = 'trapezium'

PROPERTIES = [
	Property( 'User Story' ),
	Property( 'Details' ),
	Property( 'How to test' ),
	Property( 'Estimation', regularExpression = r'^\d+\s*h|\d+\s*d|\d+\s*hours|\d+\s*days$' ),
]

CATEGORIES = [
	Category( 'Input',
		State( 'Request', showAsNew = True ),
		Transition( 'Suggest Feature', 'Feature' ),
		Transition( 'Suggest User Story', 'User Story' ),
		Transition( 'Suggest Assignment', 'Assignment' ),
	),
	Category( 'Mature',
		State( 'Feature',
			SpawnChild( 'Add User Story', 'User Story' ),
			showAsNew = True,
			plotShape = CONTAINER_STATE_SHAPE
		),
		State( 'User Story',
			SpawnChild( 'Add Task', 'Not Started Task' ),
		),
		State( 'Assignment',
			Transition( 'Convert to Task', 'Not Started Task' ),
			Transition( 'Convert to Unplanned Task', 'Unplanned Not Started Task' ),
			SpawnChild( 'Add Task', 'Not Started Task' ),
			SpawnChild( 'Add Unplanned Task', 'Unplanned Not Started Task' ),
			showAsNew = True,
			plotShape = CONTAINER_STATE_SHAPE
		),
	),
	Category( 'Tasks',
		State( 'Not Started Task',
			Transition( 'Start Working', 'Task In Progress' ),
			RequireProperty( 'Estimation' ),
		),
		State( 'Task In Progress',
			Transition( 'Done', 'Done Task' ),
			Transition( 'Pause Work', 'Paused Task' ),
			RequireProperty( 'Estimation' ),
		),
		State( 'Paused Task',
			Transition( 'Resume Working', 'Task In Progress' ),
			RequireProperty( 'Estimation' ),
		),
		State( 'Unplanned Not Started Task',
			Transition( 'Start Working', 'Unplanned Task In Progress' ),
		),
		State( 'Unplanned Task In Progress',
			Transition( 'Done', 'Unplanned Done Task' ),
			Transition( 'Pause Work', 'Paused Unplanned Task' ),
			),
		State( 'Paused Unplanned Task',
			Transition( 'Resume Working', 'Unplanned Task In Progress' ),
		),
	),
	Category( 'Planning',
		State( 'Epic Feature',
			showAsNew = True,
			plotShape = CONTAINER_STATE_SHAPE
		),
		State( 'Sprint',
			showAsNew = True,
			plotShape = CONTAINER_STATE_SHAPE
		),
	),
	Category( 'Past',
		State( 'Done Task',
			Transition( 'Resume Working', 'Task In Progress' ),
			plotShape = DEFINITIVE_STATE_SHAPE
		),
		State( 'Unplanned Done Task',
			Transition( 'Resume Working', 'Unplanned Task In Progress' ),
			plotShape = DEFINITIVE_STATE_SHAPE
		),
		State( 'Discarded', plotShape = DEFINITIVE_STATE_SHAPE ),
	),
]
