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
      <div>
        <div className="field searchfield has-addons">
          <p className="control">
            <button className={publicButton ? "button is-info is-selected" : "button"} onClick={this.handlePublicButtonClick}>
              <span>Public</span>
            </button>
          </p>
          <p className="control">
            <button className={publicPrivateButton ? "button is-info is-selected" : "button"} onClick={this.handlePublicPrivateButtonClick}>
              <span>Public & Private</span>
            </button>
          </p>
          <p className="control">
            <button className={privateButton ? "button is-info is-selected" : "button"} onClick={this.handlePrivateButtonClick}>
              <span>Private</span>
            </button>
          </p>
        </div>
        <div className="panel">
          <p className="panel-heading">
            Minimum Size In Hectares
          </p>
          <div className="panel-block">
            <p className="control has-icons-left">
              <input
                className="input"
                type="text"
                placeholder={this.props.placeholder}
                onChange={this.handleChange}
                value={this.props.sizeFormData}
                name={this.props.name}
                />
            </p>
          </div>
          <div className="panel-block">
            <button
              className="button is-link is-outlined is-fullwidth"
              onClick={this.handleRecalculate}>
              Recalculate
            </button>
          </div>

        </div>
      </div>
    )
  }
}

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
