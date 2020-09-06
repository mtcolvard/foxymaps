import React from 'react'

export default class ExploreOptions extends React.Component {
  constructor() {
    super()
    this.handlePublicButtonClick = this.handlePublicButtonClick.bind(this)
    this.handlePublicPrivateButtonClick = this.handlePublicPrivateButtonClick.bind(this)
    this.handlePrivateButtonClick = this.handlePrivateButtonClick.bind(this)
    this.handleChange = this.handleChange.bind(this)
    this.handleRecalculate = this.handleRecalculate.bind(this)
  }

  handlePublicButtonClick() {
    this.props.onHandleExploreOptionsButtonClick('publicButton')
  }
  handlePublicPrivateButtonClick() {
    this.props.onHandleExploreOptionsButtonClick('publicPrivateButton')
  }
  handlePrivateButtonClick() {
    this.props.onHandleExploreOptionsButtonClick('privateButton')
  }
  handleChange(e) {
    this.props.onHandleChange(e)
  }
  handleRecalculate(e) {
    this.props.onHandleRecalculate()
  }
  render() {
    const {privateButton, publicPrivateButton, publicButton} = this.props
    return(
      <div className="bottomFormContainer">
        <div className="panel-fix">
        <div className="panel">
          <div className="panel-tabs">
            <p className="control">
              <a className={publicButton ? "button panel-buttons is-info is-selected" : "button panel-buttons"} onClick={this.handlePublicButtonClick}>
                <span>Public</span>
              </a>
            </p>
            <p className="control">
              <a className={publicPrivateButton ? "button panel-buttons is-info is-selected" : "button panel-buttons"} onClick={this.handlePublicPrivateButtonClick}>
                <span>Public & Private</span>
              </a>
            </p>
            <p className="control">
              <a className={privateButton ? "button panel-buttons is-info is-selected" : "button panel-buttons"} onClick={this.handlePrivateButtonClick}>
                <span>Private</span>
              </a>
            </p>
          </div>
          <div className="panel-block panel-block-fix">
            <p className="panelLabels panelLabelLeft">
              Park Size (min)
            </p>
            <div className="panelInputFrame">
              <p className="control">
                <input
                  className="input panelInput"
                  type="text"
                  onChange={this.handleChange}
                  placeholder={this.props.sizeFormData}
                  value={this.props.sizeFormData}
                  name={this.props.sizeName}
                  />
              </p>
            </div>
            <p className="panelLabels panelLabelRight">
              hectares
            </p>
          </div>
          <div className="panel-block panel-block-fix">
            <p className="panelLabels panelLabelLeft">
              Rambling Tolerance
            </p>
            <div className="panelInputFrame">
              <p className="control">
                <input
                  className="input panelInput"
                  type="text"
                  onChange={this.handleChange}
                  placeholder={this.props.ramblingTolerance}
                  value={this.props.ramblingTolerance}
                  name={this.props.ramblingName}
                  />
              </p>
            </div>
            <p className="panelLabels panelLabelRight">
              meters
            </p>
          </div>
          <div className="panel-block panel-block-fix">
            <p className="panelLabels panelLabelLeft">
              Parks Along Route are within:
            </p>
            <div className="panelInputFrame">
              <p className="control">
                <input
                  className="input panelInput"
                  type="text"
                  onChange={this.handleChange}
                  placeholder={this.props.angleFilter}
                  value={this.props.angleFilter}
                  name={this.props.angleFilterName}
                  />
              </p>
            </div>
            <p className="panelLabels panelLabelRight">
              degrees
            </p>
          </div>
          <div className="panel-block">
            <button
              className="button is-link is-outlined is-fullwidth"
              onClick={this.handleRecalculate}>
              Recalculate Route
            </button>
          </div>
        </div>
        </div>
      </div>
    )
  }
}

// <p className="control">
//   <button className={publicButton ? "button is-info is-selected" : "button"} onClick={this.handlePublicButtonClick}>
//     <span>Public</span>
//   </button>
// </p>
// <p className="control">
//   <button className={publicPrivateButton ? "button is-info is-selected" : "button"} onClick={this.handlePublicPrivateButtonClick}>
//     <span>Public & Private</span>
//   </button>
// </p>
// <p className="control">
//   <button className={privateButton ? "button is-info is-selected" : "button"} onClick={this.handlePrivateButtonClick}>
//     <span>Private</span>
//   </button>
// </p>

// <div class="tabs is-toggle">
//   <ul>
//     <li class="is-active">
//       <a>
//         <span class="icon is-small"><i class="fas fa-image" aria-hidden="true"></i></span>
//         <span>Pictures</span>
//       </a>
//     </li>
//     <li>
//       <a>
//         <span class="icon is-small"><i class="fas fa-music" aria-hidden="true"></i></span>
//         <span>Music</span>
//       </a>
//     </li>
//     <li>
//       <a>
//         <span class="icon is-small"><i class="fas fa-film" aria-hidden="true"></i></span>
//         <span>Videos</span>
//       </a>
//     </li>
//     <li>
//       <a>
//         <span class="icon is-small"><i class="far fa-file-alt" aria-hidden="true"></i></span>
//         <span>Documents</span>
//       </a>
//     </li>
//   </ul>
// </div>



// <div className="field has-addons">            </div>


// <p className="panel-heading">
//   Minimum Size In Hectares
// </p>

// handleDisplayAllParks() {
//   this.props.onHandleDisplayAllParks()
// }
// <label className="panel-block">
//   <input
//     type="checkbox"
//     onClick={this.handleDisplayAllParks}
//   />
//   Display all parks within Rambling Distance
// </label>


// <div className="panel-block">
//   <p className="control has-icons-left">
//     <input className="input" type="text" placeholder="Search">
//     <span className="icon is-left">
//       <i className="fas fa-search" aria-hidden="true"></i>
//     </span>
//   </p>
// </div>
// <p className="panel-tabs">
//   <a className="is-active">All</a>
//   <a>Public</a>
//   <a>Private</a>
//   <a>Sources</a>
//   <a>Forks</a>
// </p>


// <div className="panel">
//   <p className="panel-heading">
//     Type of Site
//   </p>
//   <label className="panel-block">
//     <input type="checkbox"/>
//     Cemeteries
//   </label>
//   <label className="panel-block">
//     <input type="checkbox"/>
//     Churchyards
//   </label>
//   <label className="panel-block">
//     <input type="checkbox"/>
//     Garden Squares
//   </label>
//   <div className="panel-block">
//     <button className="button is-link is-outlined is-fullwidth">
//       Reset all filters
//     </button>
//   </div>
// </div>
//
