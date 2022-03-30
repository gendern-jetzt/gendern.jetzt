import React from "react";
import {
  Editor,
  EditorState,
  CompositeDecorator,
  ContentState,
  Modifier,
  SelectionState
} from "draft-js";
import "./EditorContainer.css";
import { TailSpin } from  'react-loader-spinner'
import "react-loader-spinner/dist/loader/css/react-spinner-loader.css";

class EditorContainer extends React.Component {
  constructor(props) {
    super(props);

    const compositeDecorator = createDecorator();

    this.state = {
      editorState: EditorState.createEmpty(compositeDecorator),
      loading: false
    };
  }

  onChange = (editorState) => {
    this.setState({ editorState });
  };

  getEntities = () => {
    let contentState = this.state.editorState.getCurrentContent();
    clearEntityRanges(contentState)
    contentState.getBlockMap().forEach(block => {
      const blockKey = block.getKey();
      const blockText = block.getText();
      this.fetchData(blockText).then((data) => {
        if (data.matches.length >= 1) {
          for (let i = 0; i < data.matches.length; i++) {
            contentState = this.state.editorState.getCurrentContent();
            const start = data.matches[i].offset
            const end = data.matches[i].offset + data.matches[i].length
            let selection = createSelectionState(blockKey, start, end);
            const contentStateWithEntity = contentState.createEntity('YES', 'IMMUTABLE');
            const entityKey = contentStateWithEntity.getLastCreatedEntityKey();
            const contentStateWithLink = Modifier.applyEntity(
              contentStateWithEntity,
              selection,
              entityKey,
            );
            const newEditorState = EditorState.createWithContent(
              contentStateWithLink,
              createDecorator()
            );
            this.setState({ editorState: newEditorState });
          }
        }
      })
    })

  }

  async fetchData(text) {
    this.setState((prevState) => ({
      ...prevState,
      loading: true,
    }));
    const response = await fetch("https://app.gendern.jetzt/check", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ text: text }),
    });
    const data = await response.json();
    this.setState((prevState) => ({
      ...prevState,
      loading: false,
    }));
    return data;
  }

  render() {
    let checkField;
    if(this.state.loading){
      checkField = <TailSpin color="#696969" height={40} width={40}/>
    }
    else {
      checkField =  <button className="btn check-btn" onClick={this.onCheckClick}>
                      Check
                    </button>
    }
    return (
      <div className="editor">
        <div>
          <div className="btn-toolbar">
            <button className="btn copy-btn" onClick={this.onCopyClick}>
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512">
                <path
                  fill="currentColor"
                  d="M433.941 65.941l-51.882-51.882A48 48 0 0 0 348.118 0H176c-26.51 0-48 21.49-48 48v48H48c-26.51 0-48 21.49-48 48v320c0 26.51 21.49 48 48 48h224c26.51 0 48-21.49 48-48v-48h80c26.51 0 48-21.49 48-48V99.882a48 48 0 0 0-14.059-33.941zM266 464H54a6 6 0 0 1-6-6V150a6 6 0 0 1 6-6h74v224c0 26.51 21.49 48 48 48h96v42a6 6 0 0 1-6 6zm128-96H182a6 6 0 0 1-6-6V54a6 6 0 0 1 6-6h106v88c0 13.255 10.745 24 24 24h88v202a6 6 0 0 1-6 6zm6-256h-64V48h9.632c1.591 0 3.117.632 4.243 1.757l48.368 48.368a6 6 0 0 1 1.757 4.243V112z"
                ></path>
              </svg>
            </button>
            <button className="btn clear-btn" onClick={this.onClearClick}>
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512">
                <path
                  fill="currentColor"
                  d="M268 416h24a12 12 0 0 0 12-12V188a12 12 0 0 0-12-12h-24a12 12 0 0 0-12 12v216a12 12 0 0 0 12 12zM432 80h-82.41l-34-56.7A48 48 0 0 0 274.41 0H173.59a48 48 0 0 0-41.16 23.3L98.41 80H16A16 16 0 0 0 0 96v16a16 16 0 0 0 16 16h16v336a48 48 0 0 0 48 48h288a48 48 0 0 0 48-48V128h16a16 16 0 0 0 16-16V96a16 16 0 0 0-16-16zM171.84 50.91A6 6 0 0 1 177 48h94a6 6 0 0 1 5.15 2.91L293.61 80H154.39zM368 464H80V128h288zm-212-48h24a12 12 0 0 0 12-12V188a12 12 0 0 0-12-12h-24a12 12 0 0 0-12 12v216a12 12 0 0 0 12 12z"
                ></path>
              </svg>
            </button>
          </div>

          <Editor
            editorState={this.state.editorState}
            onChange={this.onChange}
            placeholder="Gib hier deinen Text ein"
          />
        </div>
        <div className="check-toolbar">
          <button className="btn check-btn" onClick={this.onCheckClick}>
              {checkField}
            </button>
        </div>
      </div>
    );
  }

  onCopyClick = () => {
    let text = this.state.editorState
      .getCurrentContent()
      .getPlainText("\u0001");
    navigator.clipboard.writeText(text);
  };

  onClearClick = () => {
    const editorState = EditorState.push(
      this.state.editorState,
      ContentState.createFromText(""),
      "remove-range"
    );
    this.setState({ editorState });
  };

  onCheckClick = () => {
    this.getEntities(this.editorState);
  };
}

const yesSpan = (props) => {
  return (
    <span className="yes" data-offset-key={props.offsetKey}>
      {props.children}
    </span>
  );
};

function createDecorator() {
  return new CompositeDecorator([
    {
      strategy: yesStrategy,
      component: yesSpan,
    }
  ]);
}

function yesStrategy(contentBlock, callback, contentState) {
  contentBlock.findEntityRanges(
    (character) => {
      const entityKey = character.getEntity();
      return (
        entityKey !== null &&
        contentState.getEntity(entityKey).getType() === "YES"
      );
    },
    callback
  );
};

function createSelectionState(blockKey, startOffset, endoffset) {
  return SelectionState.createEmpty(blockKey).merge({
    anchorKey: blockKey,
    anchorOffset: startOffset,
    focusKey:blockKey,
    focusOffset: endoffset
  })
}

function clearEntityRanges(contentState){
  contentState.getBlockMap().forEach(block => {
    const blockKey = block.getKey();
    const blockText = block.getText();
    const selection = SelectionState.createEmpty(blockKey);
    const updatedSelection = selection.merge({
      anchorOffset: 0,
      focusOffset: blockText.length
    })
    Modifier.applyEntity(contentState, updatedSelection, null);
  });
  return contentState
}

export default EditorContainer;
