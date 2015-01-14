% rebase("_basicpage", title='Блог')
<div class="row">
  <div class="col-md-12"  style="margin-top:50px;">
    &nbsp;
  </div>
</div>
<div class="row">
  <div class="col-md-12">
    <h1 class="page-header">Блог о спорте, питании и образе жизни.</h1>
  </div>
</div>
<div class="row">
  <div class="col-sm-12 col-md-9">
    % if len(posts)>0:
      % for post in posts:
        <div class="post" id="{{post.post_id()}}">
          <div class="post_tags">
            % for tag in post.tags():
              <span class="post_tag" id="{{post.post_id()}}_{{tag.tag_id()}}">
                <a href="/blog/tag/{{tag.tag_id()}}">{{tag.title()}}</a>
              </span>
            % end
          </div>
          <div class="blog_post">
            {{!post.content().split('<!-- my page break -->')[0]}}
            <p><a href="/blog/{{post.post_id()}}">Читать далее...</a></p>
          </div>
        </div>
      % end
    % else:
      Постов нет
    % end
  </div>
  <div class="col-md-3 visible-lg visible-md">
    <div class="panel panel-default tag_toolbar">
      <div class="panel-body">
        <p class="lead">Теги</p>
        <p>
          % for tag in alltags:
            % tag, count = tag
            <a href="/blog/tag/{{tag.tag_id()}}">{{tag.title()}}  ({{count}})</a>
            <br>
          % end
        </p>
      </div>
    </div>
  </div>
</div>